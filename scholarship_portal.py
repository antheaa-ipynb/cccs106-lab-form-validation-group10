"""
CCCS 106: Application Development and Emerging Technologies
Week 5 Laboratory Task: CSPC Scholarship Intake Portal
Instructor: Allan O. Ibo, Jr., MSc

Instructions:
  Complete the TODO blocks in Tier 1 and Tier 2.
Target Framework: Flet v0.86.5 (Python 3.12+)
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Tuple
import flet as ft


# ============================================================================
# TIER 3: DOMAIN DATA CONTRACT & CUSTOM EXCEPTIONS
# ============================================================================

class ScholarshipValidationError(Exception):
    """Base exception for all scholarship domain validation errors."""
    pass


class IDFormatError(ScholarshipValidationError):
    """Raised when student ID does not conform to the CSPC format."""
    pass


class EmailDomainError(ScholarshipValidationError):
    """Raised when an email does not belong to the @cspc.edu.ph domain."""
    pass


class GWARangeError(ScholarshipValidationError):
    """Raised when GWA falls outside the 1.00 to 5.00 grading scale."""
    pass


@dataclass(frozen=True)
class ScholarshipApplicant:
    """Immutable domain contract representing a verified scholarship applicant."""
    full_name: str
    student_id: str
    email: str
    phone: str
    gwa: float
    program: str
    submitted_at: datetime = field(default_factory=datetime.now)


# ============================================================================
# TIER 2: VALIDATION ENGINE (STUDENT IMPLEMENTATION)
# ============================================================================

class ScholarshipValidator:
    """Encapsulated validation rules and regex logic for scholarship applicants."""

    # Compile Regular Expressions
    NAME_REGEX = re.compile(r"^[A-Za-z\s.\-',]{2,60}$")
    STUDENT_ID_REGEX = re.compile(r"^20\d{2}-\d{4,5}$")
    CSPC_EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@cspc\.edu\.ph$")
    PH_PHONE_REGEX = re.compile(r"^(?:\+63|0)9\d{9}$")

    @classmethod
    def sanitize_string(cls, raw: Optional[str]) -> str:
        """Strip leading/trailing whitespace defensively handling None."""
        return (raw or "").strip()

    @classmethod
    def validate_name(cls, value: Optional[str]) -> str:
        """
        Validates full name.
        Returns: Sanitized clean name.
        Raises: ScholarshipValidationError if invalid.
        """
        # TODO: Implement sanitization and pattern validation
        clean = cls.sanitize_string(value)
        if not clean:
            raise ScholarshipValidationError("Full name is required.")
        if not cls.NAME_REGEX.match(clean):
            raise ScholarshipValidationError("Enter a valid name (2–60 letters, hyphens, or periods).")
        return clean

    @classmethod
    def validate_student_id(cls, value: Optional[str]) -> str:
        """
        Validates CSPC student ID format (YYYY-NNNN).
        Returns: Normalized student ID.
        Raises: IDFormatError if invalid.
        """
        # TODO: Implement ID validation using cls.STUDENT_ID_REGEX
        pass

    @classmethod
    def validate_email(cls, value: Optional[str]) -> str:
        """
        Validates institutional CSPC email address.
        Returns: Lowercased, sanitized email.
        Raises: EmailDomainError if invalid.
        """
        # TODO: Implement email validation using cls.CSPC_EMAIL_REGEX
        pass

    @classmethod
    def validate_phone(cls, value: Optional[str]) -> str:
        """
        Validates and standardizes Philippine mobile numbers to 09XXXXXXXXX.
        Returns: Normalized 11-digit phone string.
        Raises: ScholarshipValidationError if invalid.
        """
        # TODO: Implement phone validation using cls.PH_PHONE_REGEX
        pass

    @classmethod
    def validate_gwa(cls, value: Optional[str]) -> float:
        """
        Defensively parses string to float and checks 1.00 <= GWA <= 5.00.
        Returns: Parsed float value.
        Raises: GWARangeError if out of bounds or non-numeric.
        """
        # TODO: Implement defensive float parsing and range check
        pass


# ============================================================================
# TIER 1: FLET PRESENTATION LAYER
# ============================================================================

def main(page: ft.Page):
    page.title = "CSPC Scholarship Intake Portal"
    page.window.width = 620
    page.window.height = 780
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 25

    # Storage for approved applications during this session
    approved_applicants: list[ScholarshipApplicant] = []

    # UI Controls
    name_field = ft.TextField(
        label="Full Name",
        hint_text="e.g., Maria Clara Santos",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        border_radius=8
    )

    id_field = ft.TextField(
        label="Student ID Number",
        hint_text="e.g., 2024-0123",
        prefix_icon=ft.Icons.BADGE_OUTLINED,
        border_radius=8
    )

    email_field = ft.TextField(
        label="Institutional Email",
        hint_text="e.g., mclara.santos@cspc.edu.ph",
        prefix_icon=ft.Icons.ALTERNATE_EMAIL,
        border_radius=8
    )

    phone_field = ft.TextField(
        label="Philippine Mobile Number",
        hint_text="e.g., 09181234567 or +639181234567",
        prefix_icon=ft.Icons.PHONE_ANDROID_OUTLINED,
        border_radius=8
    )

    gwa_field = ft.TextField(
        label="Academic General Weighted Average (GWA)",
        hint_text="Scale: 1.00 (highest) to 5.00 (passing/failing)",
        prefix_icon=ft.Icons.GRADE_OUTLINED,
        border_radius=8
    )

    program_dropdown = ft.Dropdown(
        label="Scholarship Program",
        hint_text="Select your scholarship grant",
        leading_icon=ft.Icons.SCHOOL_OUTLINED,
        border_radius=8,
        options=[
            ft.dropdown.Option("CHED Tulong Dunong Program (TDP)"),
            ft.dropdown.Option("DOST Science & Technology Scholarship"),
            ft.dropdown.Option("CSPC Institutional Academic Scholarship"),
            ft.dropdown.Option("UniFAST Tertiary Education Subsidy (TES)"),
        ]
    )

    status_summary = ft.Text(
        value="Ready to accept applications.",
        color=ft.Colors.GREY_400,
        size=13
    )

    # ------------------------------------------------------------------------
    # REAL-TIME ERROR CLEARING HANDLERS (UX ENHANCEMENT)
    # ------------------------------------------------------------------------
    def clear_field_error(e):
        """Instantly clears error state when the user begins typing."""
        if e.control.error:
            e.control.error = None
            page.update()

    def clear_dropdown_error(e):
        """Instantly clears dropdown error state on selection."""
        if e.control.error_text:
            e.control.error_text = None
            page.update()

    name_field.on_change = clear_field_error
    id_field.on_change = clear_field_error
    email_field.on_change = clear_field_error
    phone_field.on_change = clear_field_error
    gwa_field.on_change = clear_field_error
    program_dropdown.on_change = clear_dropdown_error

    # ------------------------------------------------------------------------
    # FORM SUBMISSION & MULTI-TIER DEFENSIVE PIPELINE
    # ------------------------------------------------------------------------
    def submit_application(e):
        has_errors = False

        # Reset all error states before evaluation
        name_field.error = None
        id_field.error = None
        email_field.error = None
        phone_field.error = None
        gwa_field.error = None
        program_dropdown.error_text = None

        # 1. Validate Name
        try:
            clean_name = ScholarshipValidator.validate_name(name_field.value)
        except ScholarshipValidationError as err:
            name_field.error = str(err)
            has_errors = True

        # 2. Validate Student ID
        # TODO: Wrap validate_student_id in try...except and set id_field.error
        clean_id = None

        # 3. Validate Email
        # TODO: Wrap validate_email in try...except and set email_field.error
        clean_email = None

        # 4. Validate Phone
        # TODO: Wrap validate_phone in try...except and set phone_field.error
        clean_phone = None

        # 5. Validate GWA
        # TODO: Wrap validate_gwa in try...except and set gwa_field.error
        clean_gwa = None

        # 6. Validate Program Selection
        if not program_dropdown.value:
            program_dropdown.error_text = "Please select an accredited scholarship program."
            has_errors = True

        # If any validation errors occurred, abort and notify
        if has_errors:
            page.show_dialog(
                ft.SnackBar(
                    content=ft.Text("Validation failed: Please correct highlighted fields."),
                    bgcolor=ft.Colors.RED_700,
                    behavior=ft.SnackBarBehavior.FLOATING
                )
            )
            page.update()
            return

        # 7. All Validations Passed: Instantiate Domain Contract
        # TODO: Construct ScholarshipApplicant dataclass object
        # TODO: Append to approved_applicants list
        # TODO: Display green success SnackBar and reset form fields

        page.update()

    # Layout Assembly
    submit_button = ft.FilledButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE),
                ft.Text("Submit Scholarship Application", weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_700,
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
        height=48,
        on_click=submit_application
    )

    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.LOCAL_POLICE, size=32, color=ft.Colors.BLUE_400),
                        ft.Column(
                            controls=[
                                ft.Text("CSPC Scholarship Intake Portal", size=20, weight=ft.FontWeight.BOLD),
                                ft.Text("Office of Student Affairs & Services • Academic Year 2026–2027", size=12, color=ft.Colors.GREY_400)
                            ],
                            spacing=2
                        )
                    ]
                ),
                ft.Divider(height=20, color=ft.Colors.OUTLINE_VARIANT),
                name_field,
                id_field,
                email_field,
                phone_field,
                gwa_field,
                program_dropdown,
                ft.Container(height=10),
                submit_button,
                ft.Container(height=5),
                status_summary
            ],
            spacing=14,
            scroll=ft.ScrollMode.AUTO
        )
    )


if __name__ == "__main__":
    ft.run(main)