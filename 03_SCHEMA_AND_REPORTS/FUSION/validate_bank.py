#!/usr/bin/env python3
"""Validate a public Cuantly bank. Does not prove math or visual fidelity."""

import argparse
import base64
import hashlib
import io
import json
import re
import sys
import warnings
from pathlib import Path


MAX_BANK_BYTES = 32 * 1024 * 1024
MAX_IMAGE_CHARACTERS = 16_000_000
AREAS = {"arithmetic", "algebra", "geometry", "number_theory", "combinatorics", "probability"}
SHA256 = re.compile(r"[a-f0-9]{64}")
TAG = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*")


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def positive_int(value):
    return type(value) is int and value > 0


def reject_constant(value):
    raise ValueError(f"Non-finite JSON number: {value}")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def validate_bank(bank, raw, source_pdf=None, allow_unclassified=False):
    errors, notices, figures = [], [], []

    def check(condition, message):
        if not condition:
            errors.append(message)

    check(len(raw) <= MAX_BANK_BYTES, "Bank exceeds the reader's 32 MiB limit.")
    if not isinstance(bank, dict):
        return {"ok": False, "errors": errors + ["Root must be an object."], "warnings": notices}
    check(bank.get("schema_version") == "1.0", "schema_version must be the string 1.0.")
    check(nonempty(bank.get("source_format_reference")), "Missing source_format_reference.")
    exam = bank.get("exam")
    if not isinstance(exam, dict):
        return {"ok": False, "errors": errors + ["Missing exam object."], "warnings": notices}
    for field in ("competition", "phase", "level", "school_level", "source_file", "image_policy"):
        check(nonempty(exam.get(field)), f"exam.{field} must be a nonempty string.")
    check(positive_int(exam.get("year")), "exam.year must be a positive integer.")
    source_hash = exam.get("source_sha256")
    check(isinstance(source_hash, str) and bool(SHA256.fullmatch(source_hash)), "Invalid PDF SHA-256.")
    if source_pdf is not None:
        check(hashlib.sha256(source_pdf).hexdigest() == source_hash, "Source PDF hash does not match exam.")
    if not allow_unclassified:
        for phase in ("classification_phase", "difficulty_phase"):
            if exam.get(phase) != "completed":
                notices.append(f"exam.{phase} is not completed; review legacy or unfinished metadata.")
    problems = bank.get("problems")
    if not isinstance(problems, list) or not problems:
        return {"ok": False, "errors": errors + ["problems must be a nonempty array."], "warnings": notices}
    check(type(exam.get("problem_count")) is int and exam["problem_count"] == len(problems), "exam.problem_count mismatch.")
    ids, numbers, guided, verified_count = set(), set(), [], 0
    for index, problem in enumerate(problems, 1):
        prefix = f"problem[{index}]"
        if not isinstance(problem, dict):
            errors.append(f"{prefix}: must be an object.")
            continue
        identity = problem.get("source_id")
        if nonempty(identity):
            prefix = identity
            check(identity not in ids, f"{prefix}: duplicate source_id.")
            ids.add(identity)
        else:
            errors.append(f"{prefix}: missing source_id.")
        number = problem.get("problem_number")
        check(positive_int(number), f"{prefix}: invalid problem_number.")
        if positive_int(number):
            check(number not in numbers, f"{prefix}: duplicate problem_number.")
            numbers.add(number)
        check(positive_int(problem.get("source_page")), f"{prefix}: invalid source_page.")
        for field in ("collection", "subcategory", "language", "problem_text", "solution_text"):
            check(nonempty(problem.get(field)), f"{prefix}: missing {field}.")
        check(problem.get("collection") == exam.get("competition"), f"{prefix}: collection mismatch.")
        is_open = problem.get("format") == "open_answer"
        check(problem.get("format") in ("multiple_choice", "open_answer"), f"{prefix}: unsupported format.")
        for field in ("correct_answer", "correct_option_label"):
            value = problem.get(field)
            check(field in problem and (value is None or nonempty(value)), f"{prefix}: {field} must be string/null.")
        options = problem.get("options")
        if not isinstance(options, list):
            errors.append(f"{prefix}: options must be an array.")
            options = []
        check(not options if is_open else bool(options), f"{prefix}: open answers require empty options; multiple choice requires options.")
        labels = []
        for option in options:
            if not isinstance(option, dict):
                errors.append(f"{prefix}: option must be an object.")
                continue
            label = option.get("label")
            check(nonempty(label), f"{prefix}: missing option label.")
            check(isinstance(option.get("text"), str), f"{prefix}: option text must be a string.")
            if nonempty(label):
                labels.append(label)
        check(len(set(labels)) == len(labels), f"{prefix}: duplicate option label.")
        analysis = problem.get("option_analysis")
        if not isinstance(analysis, list):
            errors.append(f"{prefix}: option_analysis must be an array.")
            analysis = []
        analysis_labels, correct_labels = [], []
        for item in analysis:
            if not isinstance(item, dict):
                errors.append(f"{prefix}: analysis item must be an object.")
                continue
            label = item.get("label")
            if nonempty(label):
                analysis_labels.append(label)
            else:
                errors.append(f"{prefix}: invalid analysis label.")
            check(nonempty(item.get("reason")), f"{prefix}: missing option reason.")
            value = item.get("is_correct")
            check("is_correct" in item and (value is None or type(value) is bool), f"{prefix}: invalid is_correct.")
            if value is True:
                correct_labels.append(label)
        check(sorted(analysis_labels) == sorted(labels), f"{prefix}: analysis must cover every option exactly once.")
        verification = problem.get("verification")
        if not isinstance(verification, dict):
            errors.append(f"{prefix}: missing verification object.")
            verification = {}
        status = verification.get("status")
        check(nonempty(status), f"{prefix}: missing verification.status.")
        for flag in ("answer_checked", "latex_checked"):
            check(type(verification.get(flag)) is bool, f"{prefix}: {flag} must be boolean.")
        check(verification.get("all_options_checked") is None if is_open else type(verification.get("all_options_checked")) is bool, f"{prefix}: all_options_checked must be null for open answers, boolean for multiple choice.")
        if isinstance(status, str) and status.startswith("verified"):
            verified_count += 1
            label = problem.get("correct_option_label")
            if is_open:
                check(label is None and not analysis, f"{prefix}: open answers have no correct option or option analysis.")
            else:
                check(nonempty(label) and label in labels, f"{prefix}: correct label is not an option.")
                check(len(correct_labels) == 1 and correct_labels[0] == label, f"{prefix}: verified answer must be unique and match analysis.")
            check(nonempty(problem.get("correct_answer")), f"{prefix}: missing verified answer.")
            for flag in (("answer_checked", "latex_checked") if is_open else ("answer_checked", "all_options_checked", "latex_checked")):
                check(verification.get(flag) is True, f"{prefix}: verified requires {flag}=true.")
        else:
            guided.append(number)
            check(problem.get("correct_option_label") is None, f"{prefix}: guided problem must have null correct label.")
            check(nonempty(verification.get("notes")), f"{prefix}: guided problem requires an explanation in notes.")
        images = problem.get("problem_images")
        if not isinstance(images, list):
            errors.append(f"{prefix}: problem_images must be an array.")
            images = []
        check(type(problem.get("has_diagram")) is bool and problem["has_diagram"] == bool(images), f"{prefix}: has_diagram mismatch.")
        for image_index, image in enumerate(images, 1):
            location = f"{prefix}/figure[{image_index}]"
            if not isinstance(image, dict):
                errors.append(f"{location}: image must be an object.")
                continue
            for field in ("label", "source", "original_filename"):
                check(nonempty(image.get(field)), f"{location}: missing {field}.")
            check(image.get("encoding") == "base64", f"{location}: encoding must be base64.")
            mime, encoded = image.get("mime_type"), image.get("base64")
            check(mime in ("image/png", "image/jpeg"), f"{location}: unsupported MIME.")
            if not isinstance(encoded, str) or not 0 < len(encoded) <= MAX_IMAGE_CHARACTERS:
                errors.append(f"{location}: missing or oversized Base64.")
                continue
            try:
                if not re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", encoded):
                    raise ValueError("Base64 contains a prefix, whitespace or invalid characters")
                decoded = base64.b64decode(encoded, validate=True)
                digest = hashlib.sha256(decoded).hexdigest()
                check(image.get("sha256") == digest, f"{location}: image hash mismatch.")
                from PIL import Image

                with warnings.catch_warnings():
                    warnings.simplefilter("error", Image.DecompressionBombWarning)
                    with Image.open(io.BytesIO(decoded)) as bitmap:
                        actual_format, dimensions = bitmap.format, bitmap.size
                        bitmap.verify()
                    with Image.open(io.BytesIO(decoded)) as bitmap:
                        bitmap.load()
                expected_format = {"image/png": "PNG", "image/jpeg": "JPEG"}.get(mime)
                check(actual_format == expected_format, f"{location}: bytes do not match MIME.")
                check(all(positive_int(image.get(field)) for field in ("width_px", "height_px")), f"{location}: dimensions must be positive integers.")
                check(dimensions == (image.get("width_px"), image.get("height_px")), f"{location}: dimensions do not match decoded bytes.")
                figures.append({"source_id": identity, "figure": image_index, "sha256": digest, "width": dimensions[0], "height": dimensions[1]})
            except ImportError:
                errors.append(f"{location}: Pillow is required to verify image decoding.")
            except Exception as exc:
                errors.append(f"{location}: image cannot be verified ({type(exc).__name__}).")
        classification = problem.get("classification")
        if classification is None and allow_unclassified:
            continue
        if not isinstance(classification, dict):
            errors.append(f"{prefix}: missing classification.")
            continue
        primary = classification.get("primary_area")
        check(isinstance(primary, str) and primary in AREAS, f"{prefix}: unsupported primary_area.")
        secondary = classification.get("secondary_areas")
        if not isinstance(secondary, list) or not all(isinstance(area, str) for area in secondary):
            errors.append(f"{prefix}: secondary_areas must be strings in an array.")
            secondary = []
        check(set(secondary) <= AREAS and primary not in secondary and len(set(secondary)) == len(secondary), f"{prefix}: invalid secondary areas.")
        check(type(classification.get("mixed")) is bool and classification["mixed"] == bool(secondary), f"{prefix}: mixed mismatch.")
        check(classification.get("difficulty") in ("L1", "L2", "L3"), f"{prefix}: difficulty must be L1/L2/L3.")
        tags = classification.get("tags")
        check(isinstance(tags, list) and bool(tags) and all(isinstance(tag, str) and TAG.fullmatch(tag) for tag in tags), f"{prefix}: tags must be nonempty snake_case strings.")
        if isinstance(tags, list) and all(isinstance(tag, str) for tag in tags):
            check(len(set(tags)) == len(tags), f"{prefix}: duplicate tags.")
        for confidence in ("classification_confidence", "difficulty_confidence"):
            value = classification.get(confidence)
            if value is not None:
                check(type(value) in (int, float) and 0 <= value <= 1, f"{prefix}: invalid {confidence}.")
    summary = bank.get("validation_summary")
    if not isinstance(summary, dict):
        errors.append("Missing validation_summary.")
    else:
        check(type(summary.get("verified_problems")) is int and summary["verified_problems"] == verified_count, "validation_summary.verified_problems mismatch.")
        check(type(summary.get("needs_review_or_invalid")) is int and summary["needs_review_or_invalid"] == len(guided), "validation_summary.needs_review_or_invalid mismatch.")
        recorded = summary.get("needs_review_problem_numbers")
        check(isinstance(recorded, list) and all(positive_int(value) for value in recorded) and sorted(recorded) == sorted(value for value in guided if positive_int(value)), "validation_summary.needs_review_problem_numbers mismatch.")
    return {
        "ok": not errors,
        "scope": "structure_options_image_decoding_hashes_classification_only",
        "mathematical_verification": "not_performed_by_this_script",
        "visual_source_comparison": "not_performed_by_this_script",
        "latex_rendering": "not_performed_by_this_script",
        "bank_sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw), "problems": len(problems), "verified": verified_count,
        "guided": len(guided), "images": len(figures), "figures": figures,
        "errors": errors, "warnings": notices,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bank", type=Path)
    parser.add_argument("--source-pdf", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--allow-unclassified", action="store_true")
    args = parser.parse_args()
    try:
        if args.bank.stat().st_size > MAX_BANK_BYTES:
            raise ValueError("Bank exceeds the reader's 32 MiB limit")
        raw = args.bank.read_bytes()
        bank = json.loads(raw.decode("utf-8-sig"), parse_constant=reject_constant, object_pairs_hook=unique_object)
        pdf = args.source_pdf.read_bytes() if args.source_pdf else None
        report = validate_bank(bank, raw, pdf, args.allow_unclassified)
    except (OSError, UnicodeError, ValueError) as exc:
        report = {"ok": False, "errors": [str(exc)], "warnings": []}
    output = json.dumps(report, ensure_ascii=True, allow_nan=False, indent=2) + "\n"
    if args.report:
        bank_path = args.bank.resolve()
        report_path = args.report.resolve()
        input_paths = {bank_path}
        if args.source_pdf:
            input_paths.add(args.source_pdf.resolve())
        if report_path in input_paths:
            parser.error("Report must not overwrite an input file")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
