from collections import defaultdict
from typing import Callable, List, Dict, Tuple, TypeVar, Union
import views_schema
from toolz.functoolz import curry
import pandas as pd
from . import legacy

T = TypeVar("T")
NestedDicts = Dict[str,Dict[str,T]]
TimePeriodGetter = NestedDicts[Callable[[pd.DataFrame], pd.DataFrame]]
PartitionsDicts = NestedDicts[Tuple[int,int]]

get_time_period_from_dataframe = curry(lambda start, end, data: data.loc[start:end, :])

class DataPartitioner():
    def __init__(self, partitions: Union[PartitionsDicts, views_schema.Partitions]):
        if isinstance(partitions, dict):
            partitions = views_schema.Partitions.from_dict(partitions)

        self.partitions = partitions
        self._data_partition_getters: TimePeriodGetter = defaultdict(dict)

        for partition_name, partition in self.partitions.partitions.items():
            for timespan_name, timespan in partition.timespans.items():
                start, end = timespan
                self._data_partition_getters[partition_name].update({
                    timespan_name: get_time_period_from_dataframe(
                        start,end)})

    def __call__(self,
            partition_name: str,
            time_period_name: str,
            data: pd.DataFrame)-> pd.DataFrame:
        return self._data_partition_getters[partition_name][time_period_name](data)

    @classmethod
    def from_legacy_periods(cls, periods: List[legacy.Period]):
        for p in periods:
            try:
                legacy.period_object_is_valid(p)
            except AssertionError:
                raise ValueError(f"Period {p} is not a valid time period object")

        partitions = {}
        for period in periods:
            partitions[period.name] = {
                    "train": (period.train_start, period.train_end),
                    "predict": (period.predict_start, period.predict_end),
                    }

        return cls(partitions)
