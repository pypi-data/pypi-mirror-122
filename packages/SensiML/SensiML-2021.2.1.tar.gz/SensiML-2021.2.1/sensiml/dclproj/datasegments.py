class DataSegment(object):
    def __init__(self, data, segment_index, label=None, uuid=None, capture=None):
        self._metadata = ["label", "segment_index", "uuid", "capture"]
        self._label = label
        self._segment_index = segment_index
        self._uuid = uuid
        self._original_index = data.index
        self._capture = capture
        self._data = data.reset_index(drop=True)

    def plot(self, **kwargs):
        self._data.plot(title=self.__str__(), **kwargs)

    @property
    def capture(self):
        return self._capture

    @property
    def segment_index(self):
        return self._segment_index

    @property
    def label(self):
        return self._label

    @property
    def uuid(self):
        return self._uuid

    @property
    def data(self):
        return self._data

    @property
    def metadata(self):
        return {metadata: getattr(self, metadata) for metadata in self._metadata}

    def __str__(self):
        return " ".join(["{}: {}, ".format(k, v) for k, v in self.metadata.items()])


class DataSegments(dict):
    def plot(self, **kwargs):
        import matplotlib as plt

        plt.rcParams.update({"figure.max_open_warning": 0})
        for _, segment in self.items():
            segment.plot(**kwargs)


def to_datasegments(data, metdata_columns, label_column):
    """Converts a dataframe into a data segments object"""

    group_columns = metdata_columns + [label_column]
    g = data.groupby(group_columns)
    ds = DataSegments()

    data_columns = [x for x in data.columns if x not in group_columns]

    for key in g.groups.keys():

        metadata = {}
        for index, value in enumerate(group_columns):
            metadata[value] = key[index]

        tmp_df = g.get_group(key)[data_columns]

        ds[tmp_df["uuid"]] = DataSegment(tmp_df, metadata, metadata[label_column])

    return ds
