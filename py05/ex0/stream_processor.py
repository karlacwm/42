from typing import Any
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def status(self, data: Any) -> str:
        pass

    def format_output(self, result: str) -> str:
        return f"{result}"


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Numeric Processor"

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                return "Invalid numeric data."
            data_count = len(data)
            total = sum(data)
            avg = total
            if data_count:
                avg = total / data_count
            return (f"Processed {data_count} numeric values, "
                    f"sum={total}, avg={avg}")
        except TypeError as e:
            return f"Error: Failed to process numbers - {e}"
        except Exception as e:
            return f"Unexpected error: {e}"

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, int):
                    return False
            return True
        elif isinstance(data, int):
            return True
        return False

    def status(self, data: Any) -> str:
        if self.validate(data):
            return "Numeric data verified"
        return "Failed to verify numeric data"


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Text Processor"

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                return "Invalid text data."
            char_count = len(data)
            word_count = len(data.split())
            return (f"{char_count} characters, {word_count} words")
        except AttributeError as e:
            return f"Error: Failed to process text - {e}"
        except Exception as e:
            return f"Unexpected error: {e}"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        return False

    def status(self, data: Any) -> str:
        if self.validate(data):
            return "Text data verified"
        return "Failed to verify text data"

    def format_output(self, result: str) -> str:
        return f"Processed text: {result}"


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Log Processor"

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                return "Invalid log data."
            level, message = data.split(":", 1)
            level = level.strip()
            message = message.strip()
            return f"{level} level detected: {message}"
        except ValueError as e:
            return f"Error: Failed to process log - {e}"
        except Exception as e:
            return f"Unexpected error: {e}"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str) and ":" in data:
            return True
        return False

    def status(self, data: Any) -> str:
        if self.validate(data):
            return "Log data verified"
        return "Failed to verify log data"

    def format_output(self, result: str) -> str:
        if "error" in result.lower():
            return f"[ALERT] {result}"
        return f"[INFO] {result}"


def case_num() -> None:
    num_data = [1, 2, 3, 4, 5]
    num_processor = NumericProcessor()
    print(f"Initializing {num_processor.name}...")
    print(f"Processing data: {num_data}")
    print(f"Validation: {num_processor.status(num_data)}")
    output = num_processor.process(num_data)
    print(f"Output: {num_processor.format_output(output)}")
    print()


def case_text() -> None:
    text_data = "Hello Nexus World"
    text_processor = TextProcessor()
    print(f"Initializing {text_processor.name}...")
    print(f"Processing data: \"{text_data}\"")
    print(f"Validation: {text_processor.status(text_data)}")
    output = text_processor.process(text_data)
    print(f"Output: {text_processor.format_output(output)}")
    print()


def case_log() -> None:
    log_data = "ERROR: Connection timeout"
    log_processor = LogProcessor()
    print(f"Initializing {log_processor.name}...")
    print(f"Processing data: \"{log_data}\"")
    print(f"Validation: {log_processor.status(log_data)}")
    output = log_processor.process(log_data)
    print(f"Output: {log_processor.format_output(output)}")
    print()


def stream_processor() -> None:
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")
    print()
    case_num()
    case_text()
    case_log()
    print("=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")
    test_cases = [
        ([1, 2, 3], NumericProcessor()),
        ("Hello world", TextProcessor()),
        ("INFO: System ready", LogProcessor())
    ]
    test_count = 1
    for data, processor in test_cases:
        output = processor.process(data)
        print(f"Result {test_count}: {processor.format_output(output)}")
        test_count += 1
    print()
    print("Foundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    stream_processor()
