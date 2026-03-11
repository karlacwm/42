from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataStream(ABC):
    def __init__(self, stream_id: str) -> None:
        super().__init__()
        self.stream_id = stream_id
        self.type = "Generic Data"
        self.count = 0

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(
            self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        if criteria is None:
            return data_batch
        return [item for item in data_batch
                if isinstance(item, str) and criteria in item]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"stream_id": self.stream_id, "type": self.type}

    @abstractmethod
    def get_summary(self) -> str:
        pass


class SensorStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.name = "Sensor Stream"
        self.type = "Environmental Data"
        self.sensor_alert = 0
        
    def process_batch(self, data_batch: List[Any]) -> str:
        self.count = len(data_batch)
        try:
            temp_filtered = self.filter_data(data_batch, criteria="temp:")
            temp_list = [float(item.split(":")[1]) for item in temp_filtered]
            for item in temp_list:
                if item > 30.0:
                    self.sensor_alert += 1
            if not temp_list:
                return f"Sensor analysis: {self.count} readings processed"
            avg = sum(temp_list) / len(temp_list)
            return (f"Sensor analysis: {self.count} readings processed, "
                    f"avg temp: {avg:.1f}°C")
        except Exception as e:
            return f"Error processing sensor batch: {e}"

    def get_summary(self) -> str:
        return f"Sensor data: {self.count} readings processed"

class TransactionStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.name = "Transaction Stream"
        self.type = "Financial Data"
        self.large_transactions = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        self.count = len(data_batch)
        try:
            buy_filtered = self.filter_data(data_batch, criteria="buy:")
            buy_list = [int(item.split(":")[1]) for item in buy_filtered]
            sell_filtered = self.filter_data(data_batch, criteria="sell:")
            sell_list = [int(item.split(":")[1]) for item in sell_filtered]
            for item in buy_list:
                if item > 100:
                    self.large_transactions += 1
            for item in sell_list:
                if item > 100:
                    self.large_transactions += 1
            net = sum(buy_list) - sum(sell_list)
            sign = "+" if net > 0 else "-"
            return (f"Transaction analysis: {self.count} operations, "
                    f"net flow: {sign}{net} units")
        except Exception as e:
            return f"Error processing transaction batch: {e}"

    def get_summary(self) -> str:
        return f"Transaction data: {self.count} operations processed"

class EventStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.name = "Event Stream"
        self.type = "System Events"

    def process_batch(self, data_batch: List[Any]) -> str:
        self.count = len(data_batch)
        try:
            errors_list = self.filter_data(data_batch, criteria="error")
            return (f"Event analysis: {self.count} events, "
                    f"{len(errors_list)} error detected")
        except Exception as e:
            return f"Error processing event batch: {e}"

    def get_summary(self) -> str:
        return f"Event data: {self.count} events processed"

class StreamProcessor:

    def __init__(self) -> None:
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        self.streams.append(stream)

    def process_all(self, batch_map: Dict[str, List[Any]]) -> None:
        try:
            for stream in self.streams:
                data = batch_map.get(stream.stream_id)
                if data:
                    stream.process_batch(data)
                print(stream.get_summary())
        except Exception as e:
            print(f"Error processing streams: {e}")


def data_stream() -> None:
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    print()
    s_data = ["temp:22.5", "humidity:65", "pressure:1013"]
    s_stream = SensorStream("SENSOR_001")
    print(f"Initializing {s_stream.name}...\n"
          f"Stream ID: {s_stream.stream_id}, Type: {s_stream.type}\n"
          f"Processing sensor batch: [{', '.join(s_data)}]")
    print(s_stream.process_batch(s_data))
    print()

    t_data = ["buy:100", "sell:150", "buy:75"]
    t_stream = TransactionStream("TRANS_001")
    print(f"Initializing {t_stream.name}...\n"
          f"Stream ID: {t_stream.stream_id}, Type: {t_stream.type}\n"
          f"Processing transaction batch: [{', '.join(t_data)}]")
    print(t_stream.process_batch(t_data))
    print()

    e_data = ["login", "error", "logout"]
    e_stream = EventStream("EVENT_001")
    print(f"Initializing {e_stream.name}...\n"
          f"Stream ID: {e_stream.stream_id}, Type: {e_stream.type}\n"
          f"Processing event batch: [{', '.join(e_data)}]")
    print(e_stream.process_batch(e_data))
    print()

    print("=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...")
    print()
    processor = StreamProcessor()

    print("Batch 1 Results:")
    data_list = {
        "SENSOR_002": ["temp:30.5", "temp:31.0"],
        "TRANS_002": ["buy:500", "sell:20", "sell:50", "sell:90"],
        "EVENT_002": ["login", "login", "login"]}
    for stream_id, data in data_list.items():
        if "SENSOR" in stream_id:
            s_stream = SensorStream(stream_id)
            processor.add_stream(s_stream)
        elif "TRANS" in stream_id:
            t_stream = TransactionStream(stream_id)
            processor.add_stream(t_stream)
        elif "EVENT" in stream_id:
            e_stream = EventStream(stream_id)
            processor.add_stream(e_stream)

    processor.process_all(data_list)
    print()

    print("Stream filtering active: High-priority data only")
    if s_stream.sensor_alert > 1:
        sensor_alert_msg = f"{s_stream.sensor_alert} critical sensor alerts"
    else:
        sensor_alert_msg = f"{s_stream.sensor_alert} critical sensor alert"
    if t_stream.large_transactions > 1:
        transaction_alert_msg = (f"{t_stream.large_transactions} large "
                                 "transactions detected")
    else:
        transaction_alert_msg = (f"{t_stream.large_transactions} large "
                                 "transaction detected")
    print(f"Filtered results: {sensor_alert_msg}, {transaction_alert_msg}")
    print()

    print("All streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    data_stream()

