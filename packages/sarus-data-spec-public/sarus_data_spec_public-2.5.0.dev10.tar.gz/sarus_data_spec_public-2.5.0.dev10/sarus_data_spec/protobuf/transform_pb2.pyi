"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sarus_data_spec.protobuf.path_pb2
import sarus_data_spec.protobuf.scalar_pb2
import sarus_data_spec.protobuf.type_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class Transform(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class PropertiesEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text = ...
        value: typing.Text = ...
        def __init__(self,
            *,
            key : typing.Text = ...,
            value : typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"key",b"key",u"value",b"value"]) -> None: ...

    class Spec(google.protobuf.message.Message):
        """Definitions"""
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        IDENTITY_FIELD_NUMBER: builtins.int
        VARIABLE_FIELD_NUMBER: builtins.int
        COMPOSED_FIELD_NUMBER: builtins.int
        PROJECT_FIELD_NUMBER: builtins.int
        FILTER_FIELD_NUMBER: builtins.int
        SHUFFLE_FIELD_NUMBER: builtins.int
        JOIN_FIELD_NUMBER: builtins.int
        CAST_FIELD_NUMBER: builtins.int
        SAMPLE_FIELD_NUMBER: builtins.int
        USER_SETTINGS_FIELD_NUMBER: builtins.int
        PROTECT_DATASET_FIELD_NUMBER: builtins.int
        EXTERNAL_FIELD_NUMBER: builtins.int
        SYNTHETIC_FIELD_NUMBER: builtins.int
        TRANSCODE_FIELD_NUMBER: builtins.int
        INVERSE_TRANSCODE_FIELD_NUMBER: builtins.int
        GET_ITEM_FIELD_NUMBER: builtins.int
        PROTECTED_PATHS_FIELD_NUMBER: builtins.int
        AUTOMATIC_USER_SETTINGS_FIELD_NUMBER: builtins.int
        PUBLIC_PATHS_FIELD_NUMBER: builtins.int
        ASSIGN_BUDGET_FIELD_NUMBER: builtins.int
        AUTOMATIC_BUDGET_FIELD_NUMBER: builtins.int
        ATTRIBUTE_BUDGET_FIELD_NUMBER: builtins.int
        SD_BUDGET_FIELD_NUMBER: builtins.int
        DERIVE_SEED_FIELD_NUMBER: builtins.int
        GROUP_BY_PE_FIELD_NUMBER: builtins.int
        SAMPLING_RATIOS_FIELD_NUMBER: builtins.int
        SELECT_SQL_FIELD_NUMBER: builtins.int
        EXTRACT_FIELD_NUMBER: builtins.int
        RELATIONSHIP_SPEC_FIELD_NUMBER: builtins.int
        DIFFERENTIATED_SAMPLE_FIELD_NUMBER: builtins.int
        @property
        def identity(self) -> global___Transform.Identity: ...
        @property
        def variable(self) -> global___Transform.Variable: ...
        @property
        def composed(self) -> global___Transform.Composed: ...
        @property
        def project(self) -> global___Transform.Project: ...
        @property
        def filter(self) -> global___Transform.Filter: ...
        @property
        def shuffle(self) -> global___Transform.Shuffle: ...
        @property
        def join(self) -> global___Transform.Join: ...
        @property
        def cast(self) -> global___Transform.Cast: ...
        @property
        def sample(self) -> global___Transform.Sample: ...
        @property
        def user_settings(self) -> global___Transform.UserSettings: ...
        @property
        def protect_dataset(self) -> global___Transform.Protect: ...
        @property
        def external(self) -> global___Transform.External:
            """np transforms, pd transforms,..."""
            pass
        @property
        def synthetic(self) -> global___Transform.Synthetic: ...
        @property
        def transcode(self) -> global___Transform.Transcode: ...
        @property
        def inverse_transcode(self) -> global___Transform.InverseTranscode: ...
        @property
        def get_item(self) -> global___Transform.GetItem: ...
        @property
        def protected_paths(self) -> global___Transform.ProtectedPaths: ...
        @property
        def automatic_user_settings(self) -> global___Transform.AutomaticUserSettings: ...
        @property
        def public_paths(self) -> global___Transform.PublicPaths: ...
        @property
        def assign_budget(self) -> global___Transform.AssignBudget: ...
        @property
        def automatic_budget(self) -> global___Transform.AutomaticBudget: ...
        @property
        def attribute_budget(self) -> global___Transform.AttributesBudget: ...
        @property
        def sd_budget(self) -> global___Transform.SDBudget: ...
        @property
        def derive_seed(self) -> global___Transform.DeriveSeed: ...
        @property
        def group_by_pe(self) -> global___Transform.GroupByPE: ...
        @property
        def sampling_ratios(self) -> global___Transform.SamplingRatios: ...
        @property
        def select_sql(self) -> global___Transform.SelectSql: ...
        @property
        def extract(self) -> global___Transform.Extract: ...
        @property
        def relationship_spec(self) -> global___Transform.RelationshipSpec: ...
        @property
        def differentiated_sample(self) -> global___Transform.DifferentiatedSample: ...
        def __init__(self,
            *,
            identity : typing.Optional[global___Transform.Identity] = ...,
            variable : typing.Optional[global___Transform.Variable] = ...,
            composed : typing.Optional[global___Transform.Composed] = ...,
            project : typing.Optional[global___Transform.Project] = ...,
            filter : typing.Optional[global___Transform.Filter] = ...,
            shuffle : typing.Optional[global___Transform.Shuffle] = ...,
            join : typing.Optional[global___Transform.Join] = ...,
            cast : typing.Optional[global___Transform.Cast] = ...,
            sample : typing.Optional[global___Transform.Sample] = ...,
            user_settings : typing.Optional[global___Transform.UserSettings] = ...,
            protect_dataset : typing.Optional[global___Transform.Protect] = ...,
            external : typing.Optional[global___Transform.External] = ...,
            synthetic : typing.Optional[global___Transform.Synthetic] = ...,
            transcode : typing.Optional[global___Transform.Transcode] = ...,
            inverse_transcode : typing.Optional[global___Transform.InverseTranscode] = ...,
            get_item : typing.Optional[global___Transform.GetItem] = ...,
            protected_paths : typing.Optional[global___Transform.ProtectedPaths] = ...,
            automatic_user_settings : typing.Optional[global___Transform.AutomaticUserSettings] = ...,
            public_paths : typing.Optional[global___Transform.PublicPaths] = ...,
            assign_budget : typing.Optional[global___Transform.AssignBudget] = ...,
            automatic_budget : typing.Optional[global___Transform.AutomaticBudget] = ...,
            attribute_budget : typing.Optional[global___Transform.AttributesBudget] = ...,
            sd_budget : typing.Optional[global___Transform.SDBudget] = ...,
            derive_seed : typing.Optional[global___Transform.DeriveSeed] = ...,
            group_by_pe : typing.Optional[global___Transform.GroupByPE] = ...,
            sampling_ratios : typing.Optional[global___Transform.SamplingRatios] = ...,
            select_sql : typing.Optional[global___Transform.SelectSql] = ...,
            extract : typing.Optional[global___Transform.Extract] = ...,
            relationship_spec : typing.Optional[global___Transform.RelationshipSpec] = ...,
            differentiated_sample : typing.Optional[global___Transform.DifferentiatedSample] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal[u"assign_budget",b"assign_budget",u"attribute_budget",b"attribute_budget",u"automatic_budget",b"automatic_budget",u"automatic_user_settings",b"automatic_user_settings",u"cast",b"cast",u"composed",b"composed",u"derive_seed",b"derive_seed",u"differentiated_sample",b"differentiated_sample",u"external",b"external",u"extract",b"extract",u"filter",b"filter",u"get_item",b"get_item",u"group_by_pe",b"group_by_pe",u"identity",b"identity",u"inverse_transcode",b"inverse_transcode",u"join",b"join",u"project",b"project",u"protect_dataset",b"protect_dataset",u"protected_paths",b"protected_paths",u"public_paths",b"public_paths",u"relationship_spec",b"relationship_spec",u"sample",b"sample",u"sampling_ratios",b"sampling_ratios",u"sd_budget",b"sd_budget",u"select_sql",b"select_sql",u"shuffle",b"shuffle",u"spec",b"spec",u"synthetic",b"synthetic",u"transcode",b"transcode",u"user_settings",b"user_settings",u"variable",b"variable"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"assign_budget",b"assign_budget",u"attribute_budget",b"attribute_budget",u"automatic_budget",b"automatic_budget",u"automatic_user_settings",b"automatic_user_settings",u"cast",b"cast",u"composed",b"composed",u"derive_seed",b"derive_seed",u"differentiated_sample",b"differentiated_sample",u"external",b"external",u"extract",b"extract",u"filter",b"filter",u"get_item",b"get_item",u"group_by_pe",b"group_by_pe",u"identity",b"identity",u"inverse_transcode",b"inverse_transcode",u"join",b"join",u"project",b"project",u"protect_dataset",b"protect_dataset",u"protected_paths",b"protected_paths",u"public_paths",b"public_paths",u"relationship_spec",b"relationship_spec",u"sample",b"sample",u"sampling_ratios",b"sampling_ratios",u"sd_budget",b"sd_budget",u"select_sql",b"select_sql",u"shuffle",b"shuffle",u"spec",b"spec",u"synthetic",b"synthetic",u"transcode",b"transcode",u"user_settings",b"user_settings",u"variable",b"variable"]) -> None: ...
        def WhichOneof(self, oneof_group: typing_extensions.Literal[u"spec",b"spec"]) -> typing.Optional[typing_extensions.Literal["identity","variable","composed","project","filter","shuffle","join","cast","sample","user_settings","protect_dataset","external","synthetic","transcode","inverse_transcode","get_item","protected_paths","automatic_user_settings","public_paths","assign_budget","automatic_budget","attribute_budget","sd_budget","derive_seed","group_by_pe","sampling_ratios","select_sql","extract","relationship_spec","differentiated_sample"]]: ...

    class External(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        class OpIdentifier(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            STD_FIELD_NUMBER: builtins.int
            PANDAS_FIELD_NUMBER: builtins.int
            NUMPY_FIELD_NUMBER: builtins.int
            TENSORFLOW_FIELD_NUMBER: builtins.int
            SKLEARN_FIELD_NUMBER: builtins.int
            PANDAS_PROFILING_FIELD_NUMBER: builtins.int
            XGBOOST_FIELD_NUMBER: builtins.int
            SKOPT_FIELD_NUMBER: builtins.int
            IMBLEARN_FIELD_NUMBER: builtins.int
            @property
            def std(self) -> global___Transform.External.Std: ...
            @property
            def pandas(self) -> global___Transform.External.Pandas: ...
            @property
            def numpy(self) -> global___Transform.External.Numpy: ...
            @property
            def tensorflow(self) -> global___Transform.External.Tensorflow: ...
            @property
            def sklearn(self) -> global___Transform.External.Sklearn: ...
            @property
            def pandas_profiling(self) -> global___Transform.External.PandasProfiling: ...
            @property
            def xgboost(self) -> global___Transform.External.XGBoost: ...
            @property
            def skopt(self) -> global___Transform.External.Skopt: ...
            @property
            def imblearn(self) -> global___Transform.External.Imblearn: ...
            def __init__(self,
                *,
                std : typing.Optional[global___Transform.External.Std] = ...,
                pandas : typing.Optional[global___Transform.External.Pandas] = ...,
                numpy : typing.Optional[global___Transform.External.Numpy] = ...,
                tensorflow : typing.Optional[global___Transform.External.Tensorflow] = ...,
                sklearn : typing.Optional[global___Transform.External.Sklearn] = ...,
                pandas_profiling : typing.Optional[global___Transform.External.PandasProfiling] = ...,
                xgboost : typing.Optional[global___Transform.External.XGBoost] = ...,
                skopt : typing.Optional[global___Transform.External.Skopt] = ...,
                imblearn : typing.Optional[global___Transform.External.Imblearn] = ...,
                ) -> None: ...
            def HasField(self, field_name: typing_extensions.Literal[u"imblearn",b"imblearn",u"numpy",b"numpy",u"op",b"op",u"pandas",b"pandas",u"pandas_profiling",b"pandas_profiling",u"sklearn",b"sklearn",u"skopt",b"skopt",u"std",b"std",u"tensorflow",b"tensorflow",u"xgboost",b"xgboost"]) -> builtins.bool: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"imblearn",b"imblearn",u"numpy",b"numpy",u"op",b"op",u"pandas",b"pandas",u"pandas_profiling",b"pandas_profiling",u"sklearn",b"sklearn",u"skopt",b"skopt",u"std",b"std",u"tensorflow",b"tensorflow",u"xgboost",b"xgboost"]) -> None: ...
            def WhichOneof(self, oneof_group: typing_extensions.Literal[u"op",b"op"]) -> typing.Optional[typing_extensions.Literal["std","pandas","numpy","tensorflow","sklearn","pandas_profiling","xgboost","skopt","imblearn"]]: ...

        class Std(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            NAME_FIELD_NUMBER: builtins.int
            name: typing.Text = ...
            def __init__(self,
                *,
                name : typing.Text = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"name",b"name"]) -> None: ...

        class Pandas(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            NAME_FIELD_NUMBER: builtins.int
            name: typing.Text = ...
            def __init__(self,
                *,
                name : typing.Text = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"name",b"name"]) -> None: ...

        class Numpy(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            NAME_FIELD_NUMBER: builtins.int
            name: typing.Text = ...
            def __init__(self,
                *,
                name : typing.Text = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"name",b"name"]) -> None: ...

        class Tensorflow(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            NAME_FIELD_NUMBER: builtins.int
            name: typing.Text = ...
            def __init__(self,
                *,
                name : typing.Text = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"name",b"name"]) -> None: ...

        class Sklearn(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            NAME_FIELD_NUMBER: builtins.int
            name: typing.Text = ...
            def __init__(self,
                *,
                name : typing.Text = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"name",b"name"]) -> None: ...

        class PandasProfiling(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            NAME_FIELD_NUMBER: builtins.int
            name: typing.Text = ...
            def __init__(self,
                *,
                name : typing.Text = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"name",b"name"]) -> None: ...

        class XGBoost(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            NAME_FIELD_NUMBER: builtins.int
            name: typing.Text = ...
            def __init__(self,
                *,
                name : typing.Text = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"name",b"name"]) -> None: ...

        class Skopt(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            NAME_FIELD_NUMBER: builtins.int
            name: typing.Text = ...
            def __init__(self,
                *,
                name : typing.Text = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"name",b"name"]) -> None: ...

        class Imblearn(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            NAME_FIELD_NUMBER: builtins.int
            name: typing.Text = ...
            def __init__(self,
                *,
                name : typing.Text = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"name",b"name"]) -> None: ...

        ARGUMENTS_FIELD_NUMBER: builtins.int
        NAMED_ARGUMENTS_FIELD_NUMBER: builtins.int
        OP_IDENTIFIER_FIELD_NUMBER: builtins.int
        arguments: builtins.bytes = ...
        named_arguments: builtins.bytes = ...
        @property
        def op_identifier(self) -> global___Transform.External.OpIdentifier: ...
        def __init__(self,
            *,
            arguments : builtins.bytes = ...,
            named_arguments : builtins.bytes = ...,
            op_identifier : typing.Optional[global___Transform.External.OpIdentifier] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal[u"op_identifier",b"op_identifier"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"arguments",b"arguments",u"named_arguments",b"named_arguments",u"op_identifier",b"op_identifier"]) -> None: ...

    class Identity(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class Variable(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        POSITION_FIELD_NUMBER: builtins.int
        NAME_FIELD_NUMBER: builtins.int
        position: builtins.int = ...
        name: typing.Text = ...
        def __init__(self,
            *,
            position : builtins.int = ...,
            name : typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"name",b"name",u"position",b"position"]) -> None: ...

    class Composed(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        class NamedArgumentsEntry(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            KEY_FIELD_NUMBER: builtins.int
            VALUE_FIELD_NUMBER: builtins.int
            key: typing.Text = ...
            value: typing.Text = ...
            def __init__(self,
                *,
                key : typing.Text = ...,
                value : typing.Text = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"key",b"key",u"value",b"value"]) -> None: ...

        TRANSFORM_FIELD_NUMBER: builtins.int
        ARGUMENTS_FIELD_NUMBER: builtins.int
        NAMED_ARGUMENTS_FIELD_NUMBER: builtins.int
        transform: typing.Text = ...
        """Transform"""

        @property
        def arguments(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
            """Arguments of the current transform are transforms"""
            pass
        @property
        def named_arguments(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]: ...
        def __init__(self,
            *,
            transform : typing.Text = ...,
            arguments : typing.Optional[typing.Iterable[typing.Text]] = ...,
            named_arguments : typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"arguments",b"arguments",u"named_arguments",b"named_arguments",u"transform",b"transform"]) -> None: ...

    class Project(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        PROJECTION_FIELD_NUMBER: builtins.int
        @property
        def projection(self) -> sarus_data_spec.protobuf.type_pb2.Type:
            """This should be a 'supertype' the type the data can project into."""
            pass
        def __init__(self,
            *,
            projection : typing.Optional[sarus_data_spec.protobuf.type_pb2.Type] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal[u"projection",b"projection"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"projection",b"projection"]) -> None: ...

    class Filter(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        FILTER_FIELD_NUMBER: builtins.int
        @property
        def filter(self) -> sarus_data_spec.protobuf.type_pb2.Type:
            """This should be a 'subtype' the type the data can be retricted to."""
            pass
        def __init__(self,
            *,
            filter : typing.Optional[sarus_data_spec.protobuf.type_pb2.Type] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal[u"filter",b"filter"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"filter",b"filter"]) -> None: ...

    class Shuffle(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class Join(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        ON_FIELD_NUMBER: builtins.int
        @property
        def on(self) -> sarus_data_spec.protobuf.type_pb2.Type:
            """This should be a common 'supertype' between tables."""
            pass
        def __init__(self,
            *,
            on : typing.Optional[sarus_data_spec.protobuf.type_pb2.Type] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal[u"on",b"on"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"on",b"on"]) -> None: ...

    class Cast(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        TYPE_FIELD_NUMBER: builtins.int
        @property
        def type(self) -> sarus_data_spec.protobuf.type_pb2.Type:
            """Type to cast into."""
            pass
        def __init__(self,
            *,
            type : typing.Optional[sarus_data_spec.protobuf.type_pb2.Type] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal[u"type",b"type"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"type",b"type"]) -> None: ...

    class Sample(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        FRACTION_FIELD_NUMBER: builtins.int
        SIZE_FIELD_NUMBER: builtins.int
        SEED_FIELD_NUMBER: builtins.int
        fraction: builtins.float = ...
        size: builtins.int = ...
        @property
        def seed(self) -> sarus_data_spec.protobuf.scalar_pb2.Scalar: ...
        def __init__(self,
            *,
            fraction : builtins.float = ...,
            size : builtins.int = ...,
            seed : typing.Optional[sarus_data_spec.protobuf.scalar_pb2.Scalar] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal[u"fraction",b"fraction",u"proportion",b"proportion",u"seed",b"seed",u"size",b"size"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"fraction",b"fraction",u"proportion",b"proportion",u"seed",b"seed",u"size",b"size"]) -> None: ...
        def WhichOneof(self, oneof_group: typing_extensions.Literal[u"proportion",b"proportion"]) -> typing.Optional[typing_extensions.Literal["fraction","size"]]: ...

    class SchemaInference(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        class CastPolicy(_CastPolicy, metaclass=_CastPolicyEnumTypeWrapper):
            pass
        class _CastPolicy:
            V = typing.NewType('V', builtins.int)
        class _CastPolicyEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_CastPolicy.V], builtins.type):
            DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
            NONE = Transform.SchemaInference.CastPolicy.V(0)
            MOST_LIKELY = Transform.SchemaInference.CastPolicy.V(1)

        NONE = Transform.SchemaInference.CastPolicy.V(0)
        MOST_LIKELY = Transform.SchemaInference.CastPolicy.V(1)

        CAST_POLICY_FIELD_NUMBER: builtins.int
        cast_policy: global___Transform.SchemaInference.CastPolicy.V = ...
        def __init__(self,
            *,
            cast_policy : global___Transform.SchemaInference.CastPolicy.V = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"cast_policy",b"cast_policy"]) -> None: ...

    class GroupBy(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        KEY_FIELD_NUMBER: builtins.int
        key: typing.Text = ...
        def __init__(self,
            *,
            key : typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"key",b"key"]) -> None: ...

    class Synthetic(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class UserSettings(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class AutomaticUserSettings(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        MAX_CATEGORIES_FIELD_NUMBER: builtins.int
        max_categories: builtins.int = ...
        def __init__(self,
            *,
            max_categories : builtins.int = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"max_categories",b"max_categories"]) -> None: ...

    class Protect(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class Transcode(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class InverseTranscode(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class DifferentiatedSample(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        FRACTION_FIELD_NUMBER: builtins.int
        SIZE_FIELD_NUMBER: builtins.int
        SEED_FIELD_NUMBER: builtins.int
        fraction: builtins.float = ...
        size: builtins.int = ...
        @property
        def seed(self) -> sarus_data_spec.protobuf.scalar_pb2.Scalar: ...
        def __init__(self,
            *,
            fraction : builtins.float = ...,
            size : builtins.int = ...,
            seed : typing.Optional[sarus_data_spec.protobuf.scalar_pb2.Scalar] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal[u"fraction",b"fraction",u"proportion",b"proportion",u"seed",b"seed",u"size",b"size"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"fraction",b"fraction",u"proportion",b"proportion",u"seed",b"seed",u"size",b"size"]) -> None: ...
        def WhichOneof(self, oneof_group: typing_extensions.Literal[u"proportion",b"proportion"]) -> typing.Optional[typing_extensions.Literal["fraction","size"]]: ...

    class ProtectedPaths(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class PublicPaths(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class GetItem(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        PATH_FIELD_NUMBER: builtins.int
        @property
        def path(self) -> sarus_data_spec.protobuf.path_pb2.Path: ...
        def __init__(self,
            *,
            path : typing.Optional[sarus_data_spec.protobuf.path_pb2.Path] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal[u"path",b"path"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"path",b"path"]) -> None: ...

    class AssignBudget(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class AutomaticBudget(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class AttributesBudget(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class SDBudget(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class DeriveSeed(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        RANDOM_INTEGER_FIELD_NUMBER: builtins.int
        random_integer: builtins.int = ...
        def __init__(self,
            *,
            random_integer : builtins.int = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"random_integer",b"random_integer"]) -> None: ...

    class GroupByPE(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class SamplingRatios(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class RelationshipSpec(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        def __init__(self,
            ) -> None: ...

    class SelectSql(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        class SQLDialect(_SQLDialect, metaclass=_SQLDialectEnumTypeWrapper):
            pass
        class _SQLDialect:
            V = typing.NewType('V', builtins.int)
        class _SQLDialectEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_SQLDialect.V], builtins.type):
            DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
            NONE = Transform.SelectSql.SQLDialect.V(0)
            POSTGRES = Transform.SelectSql.SQLDialect.V(1)
            SQL_SERVER = Transform.SelectSql.SQLDialect.V(2)
            MY_SQL = Transform.SelectSql.SQLDialect.V(3)
            SQLLITE = Transform.SelectSql.SQLDialect.V(4)
            ORACLE = Transform.SelectSql.SQLDialect.V(5)
            BIG_QUERY = Transform.SelectSql.SQLDialect.V(6)
            REDSHIFT = Transform.SelectSql.SQLDialect.V(7)
            HIVE = Transform.SelectSql.SQLDialect.V(8)

        NONE = Transform.SelectSql.SQLDialect.V(0)
        POSTGRES = Transform.SelectSql.SQLDialect.V(1)
        SQL_SERVER = Transform.SelectSql.SQLDialect.V(2)
        MY_SQL = Transform.SelectSql.SQLDialect.V(3)
        SQLLITE = Transform.SelectSql.SQLDialect.V(4)
        ORACLE = Transform.SelectSql.SQLDialect.V(5)
        BIG_QUERY = Transform.SelectSql.SQLDialect.V(6)
        REDSHIFT = Transform.SelectSql.SQLDialect.V(7)
        HIVE = Transform.SelectSql.SQLDialect.V(8)

        class AliasedQueries(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            ALIASED_QUERY_FIELD_NUMBER: builtins.int
            @property
            def aliased_query(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Transform.SelectSql.AliasedQuery]: ...
            def __init__(self,
                *,
                aliased_query : typing.Optional[typing.Iterable[global___Transform.SelectSql.AliasedQuery]] = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"aliased_query",b"aliased_query"]) -> None: ...

        class AliasedQuery(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            PATH_FIELD_NUMBER: builtins.int
            QUERY_FIELD_NUMBER: builtins.int
            @property
            def path(self) -> sarus_data_spec.protobuf.path_pb2.Path: ...
            query: typing.Text = ...
            def __init__(self,
                *,
                path : typing.Optional[sarus_data_spec.protobuf.path_pb2.Path] = ...,
                query : typing.Text = ...,
                ) -> None: ...
            def HasField(self, field_name: typing_extensions.Literal[u"path",b"path"]) -> builtins.bool: ...
            def ClearField(self, field_name: typing_extensions.Literal[u"path",b"path",u"query",b"query"]) -> None: ...

        QUERY_FIELD_NUMBER: builtins.int
        ALIASED_QUERIES_FIELD_NUMBER: builtins.int
        SQL_DIALECT_FIELD_NUMBER: builtins.int
        query: typing.Text = ...
        @property
        def aliased_queries(self) -> global___Transform.SelectSql.AliasedQueries: ...
        sql_dialect: global___Transform.SelectSql.SQLDialect.V = ...
        def __init__(self,
            *,
            query : typing.Text = ...,
            aliased_queries : typing.Optional[global___Transform.SelectSql.AliasedQueries] = ...,
            sql_dialect : global___Transform.SelectSql.SQLDialect.V = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal[u"aliased_queries",b"aliased_queries",u"query",b"query",u"select",b"select"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"aliased_queries",b"aliased_queries",u"query",b"query",u"select",b"select",u"sql_dialect",b"sql_dialect"]) -> None: ...
        def WhichOneof(self, oneof_group: typing_extensions.Literal[u"select",b"select"]) -> typing.Optional[typing_extensions.Literal["query","aliased_queries"]]: ...

    class Extract(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        SIZE_FIELD_NUMBER: builtins.int
        size: builtins.int = ...
        def __init__(self,
            *,
            size : builtins.int = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal[u"size",b"size"]) -> None: ...

    UUID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    DOC_FIELD_NUMBER: builtins.int
    SPEC_FIELD_NUMBER: builtins.int
    PROPERTIES_FIELD_NUMBER: builtins.int
    INVERSIBLE_FIELD_NUMBER: builtins.int
    SCHEMA_PRESERVING_FIELD_NUMBER: builtins.int
    uuid: typing.Text = ...
    """A dataset transform
    e.g. RFC 4122 id used to refer to the transform
    """

    name: typing.Text = ...
    doc: typing.Text = ...
    @property
    def spec(self) -> global___Transform.Spec: ...
    @property
    def properties(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]:
        """Other properties"""
        pass
    inversible: builtins.bool = ...
    schema_preserving: builtins.bool = ...
    def __init__(self,
        *,
        uuid : typing.Text = ...,
        name : typing.Text = ...,
        doc : typing.Text = ...,
        spec : typing.Optional[global___Transform.Spec] = ...,
        properties : typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        inversible : builtins.bool = ...,
        schema_preserving : builtins.bool = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal[u"spec",b"spec"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal[u"doc",b"doc",u"inversible",b"inversible",u"name",b"name",u"properties",b"properties",u"schema_preserving",b"schema_preserving",u"spec",b"spec",u"uuid",b"uuid"]) -> None: ...
global___Transform = Transform
