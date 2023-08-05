import typing as t

import numpy as np
import pyarrow as pa

from sarus_data_spec.arrow.array import convert_record_batch
from sarus_data_spec.bounds import bounds as bounds_builder
from sarus_data_spec.constants import DATA, DATASET_SLUGNAME
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.ops.asyncio.processor.standard.sample import (
    fast_gather,
    new_sampling_ratio,
    sample_arrow_to_arrow,
)
from sarus_data_spec.manager.ops.asyncio.processor.standard.sampling.size_utils import (  # noqa: E501
    differentiated_sampled_size,
    sampled_size,
)
from sarus_data_spec.manager.ops.asyncio.processor.standard.standard_op import (  # noqa: E501
    StandardDatasetOp,
)
from sarus_data_spec.marginals import marginals as marginals_builder
from sarus_data_spec.path import straight_path
from sarus_data_spec.scalar import Scalar
from sarus_data_spec.schema import schema
from sarus_data_spec.size import size as size_builder
import sarus_data_spec.typing as st

try:
    from sarus_data_spec.manager.ops.asyncio.processor.standard.sampling.differentiated_sampling_sizes import (  # noqa: E501
        differentiated_sampling_sizes,
    )
    from sarus_data_spec.manager.ops.asyncio.processor.standard.sampling.sql import (  # noqa: E501
        sql_differentiated_sample_to_arrow,
    )
except ModuleNotFoundError as exception:
    # for the public repo
    if (
        exception.name
        == 'sarus_data_spec.manager.ops.asyncio.processor.standard.sampling'  # noqa: E501
    ):
        pass
    else:
        raise exception


class DifferentiatedSample(StandardDatasetOp):
    """Computes schema and arrow
    batches for a dataspec transformed by
    a differentiated transform
    """

    async def size(self) -> st.Size:
        parent_size = await self.parent_size()

        previous_schema = await self.parent_schema()
        if len(previous_schema.tables()) == 1:
            size_ratio = new_sampling_ratio(
                self.dataset, parent_size.statistics()
            )
            if size_ratio >= 1:
                return parent_size
            return size_builder(
                self.dataset,
                sampled_size(parent_size.statistics(), size_ratio),
            )
        size_dict = await differentiated_sampling_sizes(self.dataset)
        return size_builder(
            self.dataset,
            differentiated_sampled_size(
                parent_size.statistics(), size_dict, curr_path=[DATA]
            ),
        )

    async def bounds(self) -> st.Bounds:
        parent_bounds = await self.parent_bounds()
        previous_schema = await self.parent_schema()
        if len(previous_schema.tables()) == 1:
            size_ratio = new_sampling_ratio(
                self.dataset, parent_bounds.statistics()
            )

            if size_ratio >= 1:
                return parent_bounds

            return bounds_builder(
                self.dataset,
                sampled_size(parent_bounds.statistics(), size_ratio),
            )

        size_dict = await differentiated_sampling_sizes(self.dataset)
        return bounds_builder(
            self.dataset,
            differentiated_sampled_size(
                parent_bounds.statistics(), size_dict, curr_path=[DATA]
            ),
        )

    async def marginals(self) -> st.Marginals:
        parent_marginals = await self.parent_marginals()
        previous_schema = await self.parent_schema()
        if len(previous_schema.tables()) == 1:
            size_ratio = new_sampling_ratio(
                self.dataset, parent_marginals.statistics()
            )

            if size_ratio >= 1:
                return parent_marginals

            return marginals_builder(
                self.dataset,
                sampled_size(parent_marginals.statistics(), size_ratio),
            )

        size_dict = await differentiated_sampling_sizes(self.dataset)
        return marginals_builder(
            self.dataset,
            differentiated_sampled_size(
                parent_marginals.statistics(), size_dict, curr_path=[DATA]
            ),
        )

    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        return schema(
            self.dataset,
            schema_type=parent_schema.type(),
            protected_paths=parent_schema.protobuf().protected,
            properties=parent_schema.properties(),
            name=self.dataset.properties().get(DATASET_SLUGNAME, None),
        )

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        parent = t.cast(Dataset, self.parent())
        if parent.manager().is_big_data(parent):
            return await sql_differentiated_sample_to_arrow(
                self.dataset, batch_size
            )
        return await self._arrow_to_arrow(batch_size)

    async def _arrow_to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        seed = Scalar(
            self.dataset.transform().protobuf().spec.differentiated_sample.seed
        ).value()
        generator = np.random.default_rng(seed)

        previous_ds = t.cast(Dataset, self.parent())
        previous_schema = await self.parent_schema()
        parent_batches = [
            convert_record_batch(batch, previous_schema.type())
            async for batch in await self.parent_to_arrow()
        ]
        struct_arr = pa.concat_arrays(parent_batches)
        previous_size = await previous_ds.manager().async_size(previous_ds)
        assert previous_size

        if len(previous_schema.tables()) == 1:
            return await sample_arrow_to_arrow(self, batch_size)

        size_dict = await differentiated_sampling_sizes(self.dataset)

        indices_to_take = sample_indices_from_array(
            array=struct_arr.field(DATA),
            stat=previous_size.statistics(),
            selected_indices=pa.array(
                np.linspace(0, len(struct_arr) - 1, len(struct_arr), dtype=int)
            ),
            new_size_dict=size_dict,
            curr_path=[DATA],
            random_gen=generator,
        )

        return fast_gather(
            indices=indices_to_take.to_numpy(),
            batches=pa.Table.from_arrays(
                struct_arr.flatten(),
                names=list(previous_schema.type().children().keys()),
            ).to_batches(max_chunksize=1000),
            batch_size=batch_size,
        )


def sample_indices_from_array(
    array: pa.Array,
    stat: st.Statistics,
    selected_indices: pa.Array,
    new_size_dict: t.Dict[st.Path, int],
    random_gen: np.random.Generator,
    curr_path: t.List[str],
) -> pa.Array:
    class IndicesSampler(st.StatisticsVisitor):

        indices: pa.Array = selected_indices
        batch_array: pa.Array = array

        def Union(
            self,
            fields: t.Mapping[str, st.Statistics],
            size: int,
            multiplicity: float,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:

            new_indices = []
            for field, field_stat in fields.items():
                filter_idex = pa.array(
                    np.equal(
                        self.batch_array.field('field_selected'),
                        np.array(field),
                    )
                )
                updated_indices = sample_indices_from_array(
                    self.batch_array.filter(filter_idex).field(field),
                    field_stat,
                    self.indices.filter(filter_idex),
                    new_size_dict,
                    random_gen,
                    [*(el for el in curr_path), field],
                )
                new_indices.append(updated_indices)
            self.indices = pa.concat_arrays(new_indices)

        def Struct(
            self,
            fields: t.Mapping[str, st.Statistics],
            size: int,
            multiplicity: float,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:

            # sample indices to size and sample ratio
            new_size = new_size_dict[straight_path(curr_path.copy())]
            self.indices = pa.array(
                random_gen.choice(
                    self.indices,
                    replace=False,
                    size=min(new_size, size, len(array)),
                )
            )  # need to put array otherwise because of dp
            # we can have size and new size larger and an error will be raised

        def Null(self, size: int, multiplicity: float) -> None:
            raise NotImplementedError

        def Unit(self, size: int, multiplicity: float) -> None:
            raise NotImplementedError

        def Boolean(
            self,
            size: int,
            multiplicity: float,
            probabilities: t.Optional[t.List[float]] = None,
            names: t.Optional[t.List[bool]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Id(self, size: int, multiplicity: float) -> None:
            raise NotImplementedError

        def Integer(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Enum(
            self,
            size: int,
            multiplicity: float,
            probabilities: t.Optional[t.List[float]] = None,
            names: t.Optional[t.List[str]] = None,
            values: t.Optional[t.List[float]] = None,
            name: str = 'Enum',
        ) -> None:
            raise NotImplementedError

        def Float(
            self,
            size: int,
            multiplicity: float,
            min_value: float,
            max_value: float,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[float]] = None,
        ) -> None:
            raise NotImplementedError

        def Text(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            example: str = '',
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Bytes(self, size: int, multiplicity: float) -> None:
            raise NotImplementedError

        def Optional(
            self, statistics: st.Statistics, size: int, multiplicity: float
        ) -> None:
            raise NotImplementedError

        def List(
            self,
            statistics: st.Statistics,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            name: str = 'List',
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Array(
            self,
            statistics: st.Statistics,
            size: int,
            multiplicity: float,
            min_values: t.Optional[t.List[float]] = None,
            max_values: t.Optional[t.List[float]] = None,
            name: str = 'Array',
            probabilities: t.Optional[t.List[t.List[float]]] = None,
            values: t.Optional[t.List[t.List[float]]] = None,
        ) -> None:
            raise NotImplementedError

        def Datetime(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Constrained(
            self, statistics: st.Statistics, size: int, multiplicity: float
        ) -> None:
            raise NotImplementedError

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Time(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Date(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Duration(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

    visitor = IndicesSampler()
    stat.accept(visitor)
    return visitor.indices
