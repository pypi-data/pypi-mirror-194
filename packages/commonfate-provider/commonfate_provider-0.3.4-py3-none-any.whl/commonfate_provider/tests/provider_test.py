from commonfate_provider import provider, diagnostics


class BasicProvider(provider.Provider):
    pass


class ExampleProvider(provider.Provider):
    value = provider.String()


@provider.config_validator(name="List Users")
def can_list_users(provider: ExampleProvider, diagnostics: diagnostics.Logs) -> None:
    diagnostics.info("some message here")


@provider.config_validator(name="Fails")
def fails(provider: ExampleProvider, diagnostics: diagnostics.Logs) -> None:
    raise Exception("something bad happened")


def test_load_config_works():
    config = '{"value": "test"}'
    got = ExampleProvider()
    got._cf_load_config(provider.StringLoader(config))
    assert got.value.get() == "test"


def test_export_schema_works():
    got = ExampleProvider.export_schema()
    want = {"value": {"type": "string", "usage": None, "secret": False}}
    assert got == want


def test_capabilities_works():
    got = provider.capabilities(_internal_key="BasicProvider")
    want = {"builtin": {}}
    assert got == want


def test_provider_config_validation_works():
    config = '{"value": "test"}'
    prov = ExampleProvider()
    prov._cf_load_config(provider.StringLoader(config))
    got = prov._cf_validate_config()
    want = {
        "can_list_users": {
            "logs": [{"level": "info", "msg": "some message here"}],
            "success": True,
        },
        "fails": {
            "logs": [{"level": "error", "msg": "something bad happened"}],
            "success": False,
        },
    }
    assert got == want
