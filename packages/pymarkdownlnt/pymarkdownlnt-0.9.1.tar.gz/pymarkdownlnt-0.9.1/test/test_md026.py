"""
Module to provide tests related to the MD026 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

from .utils import write_temporary_configuration


@pytest.mark.rules
def test_md026_good_ends_without_punctuation_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md026/ends_without_punctuation_atx.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md026_good_ends_with_entity_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md026/ends_with_entity_atx.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md026_bad_ends_with_punctuation_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do end with a
    punctuation character.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md026/ends_with_punctuation_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md026/ends_with_punctuation_atx.md:1:18: "
        + "MD026: Trailing punctuation present in heading text. (no-trailing-punctuation)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md026_good_ends_with_punctuation_then_inline_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do end with a
    punctuation character, but after that character have an inline sequence.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md026/ends_with_punctuation_then_inline_atx.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md026_good_ends_with_punctuation_atx_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has atx headings that do end with what
    would normally be punctuation, but have configuration that changes those characters
    that are considered punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md026": {"punctuation": "?!"}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md026/ends_with_punctuation_atx.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md026_good_ends_without_punctuation_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has setext headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md026/ends_without_punctuation_setext.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md026_good_ends_with_entity_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has setext headings that do not end with
    punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md026/ends_with_entity_setext.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md026_bad_ends_with_punctuation_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has setext headings that do end with a
    punctuation character.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md026/ends_with_punctuation_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md026/ends_with_punctuation_setext.md:1:18: "
        + "MD026: Trailing punctuation present in heading text. (no-trailing-punctuation)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md026_bad_ends_with_punctuation_setext_multiline():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has setext headings that do end with a
    punctuation character.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md026/ends_with_punctuation_setext_multiline.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md026/ends_with_punctuation_setext_multiline.md:2:18: "
        + "MD026: Trailing punctuation present in heading text. (no-trailing-punctuation)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md026_good_ends_with_punctuation_then_inline_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has setext headings that do end with a
    punctuation character, but after that character have an inline sequence.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md026/ends_with_punctuation_then_inline_setext.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md026_good_ends_with_punctuation_setext_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD026 directory that has setext headings that do end with what
    would normally be punctuation, but have configuration that changes those characters
    that are considered punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md026": {"punctuation": "?!"}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md026/ends_with_punctuation_setext.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)
