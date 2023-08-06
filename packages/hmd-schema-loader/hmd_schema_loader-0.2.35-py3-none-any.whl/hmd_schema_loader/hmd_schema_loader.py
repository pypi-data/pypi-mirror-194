import glob
import importlib
import json
import os
import re
import zipimport
from importlib import import_module
from pathlib import Path
from typing import List, Union


class LoaderException(Exception):
    pass


def _validate_namespace_name(
    conf_name: str, conf_namespace: str, base: Path, def_path: Path
):
    conf_parts = (
        f"{conf_namespace}.{conf_name}" if conf_namespace else conf_name
    ).split(".")

    def_path_parts = list(def_path.relative_to(base).parts)
    def_path_parts[-1] = def_path.stem

    if conf_parts != def_path_parts:
        raise Exception(
            f"Configured namespace doesn't match file path/name: {'.'.join(conf_parts)} vs {'/'.join(def_path_parts)}.hms"
        )


def snake_to_pascal(name_in_snake):
    return "".join([n.capitalize() for n in name_in_snake.split("_")])


def extract_class(fully_qualified_name):
    parts = fully_qualified_name.rsplit(".", maxsplit=1)
    return snake_to_pascal(parts[-1])


class DefaultLoader:
    def __init__(
        self,
        base: Union[str, List[str]] = "./",
        parent=None,
        fail_on_no_class: bool = True,
    ) -> None:
        self.base = [
            os.path.expanduser(dir)
            for dir in (base if isinstance(base, list) else [base])
        ]
        self.parent = parent
        self.cache = {}
        self._duplicate_check()
        self._retrieve_remote_schemas()
        self.fail_on_no_class = fail_on_no_class

    def _retrieve_remote_schemas(self) -> None:
        new_bases = set()
        for loc in self.base:
            new_bases.add(loc)
        self.base = list(new_bases)

    def __load(self, name: str):
        looked_for = []
        for base in self.base:
            definition_path = os.path.join(*([base] + name.split(".")))
            exts = glob.glob(definition_path + ".*.hms")
            definition_path += ".hms"
            if not os.path.exists(definition_path):
                looked_for.append(definition_path)
                continue

            with open(definition_path, "r") as f:
                entity_def = json.load(f)

            for ext in exts:
                if entity_def.get("extensions") is None:
                    entity_def["extensions"] = {}
                with open(ext, "r") as ef:
                    ext_name = ext.split(".")[-2]
                    entity_def["extensions"][ext_name] = json.load(ef)

            namespace = entity_def.get("namespace")
            name = entity_def.get("name")
            _validate_namespace_name(name, namespace, base, Path(definition_path))

            fully_qualified_name = ((namespace + ".") if namespace else "") + name

            the_class = None
            try:
                module = import_module(fully_qualified_name)
                the_class = getattr(module, extract_class(fully_qualified_name))
            except ModuleNotFoundError as error:
                if self.fail_on_no_class:
                    raise error

            return {
                "entity_def": entity_def,
                "module_name": fully_qualified_name,
                "class_name": extract_class(fully_qualified_name),
                "class": the_class,
            }

        # if we get here, then it's not foound...
        raise LoaderException(
            f"No entity definition file found for namespace name, {name}. Looking for one of: {', '.join(looked_for)}."
        )

    def _get_relative_paths(self):
        for a_base in self.base:
            for base, _, files in os.walk(a_base):
                for file_ in files:
                    if file_.endswith(".hms"):
                        if re.match(r".*\.[a-zA-Z\-_]*\.hms", file_):
                            # skip extension files
                            continue
                        relative_path = os.path.join(
                            Path(base).relative_to(a_base), file_
                        )[:-4]
                        relative_path = relative_path.replace(os.sep, ".")
                        yield relative_path

    def _duplicate_check(self):
        path_set = set()
        duplicates = []
        for relative_path in self._get_relative_paths():
            if relative_path in path_set:
                duplicates.append(relative_path)
            else:
                path_set.add(relative_path)

        if duplicates:
            raise LoaderException(
                f"Duplicate schema files found: {', '.join(duplicates)}"
            )

    def load_all(self):
        for relative_path in self._get_relative_paths():
            self.get(relative_path)

    def get(self, name: str):
        result = self.cache.get(name)
        if not result:
            self.cache[name] = self.__load(name)
        result = self.cache.get(name)
        return result

    def get_class(self, name: str):
        return self.get(name)["class"]

    def __iter__(self):
        return iter(self.cache.keys())

    def __len__(self):
        return len(self.cache)


def get_schema_root(package_name: str) -> str:
    package_path = "schemas"

    package_path = os.path.normpath(package_path).rstrip(os.path.sep)

    # Make sure the package exists. This also makes namespace
    # packages work, otherwise get_loader returns None.
    import_module(package_name)
    spec = importlib.util.find_spec(package_name)
    assert spec is not None, "An import spec was not found for the package."
    loader = spec.loader
    assert loader is not None, "A loader was not found for the package."
    _archive = None
    schema_root = None

    if isinstance(loader, zipimport.zipimporter):
        _archive = loader.archive
        pkgdir = next(iter(spec.submodule_search_locations))  # type: ignore
        schema_root = os.path.join(pkgdir, package_path)
    elif spec.submodule_search_locations:
        # This will be one element for regular packages and multiple
        # for namespace packages.
        for root in spec.submodule_search_locations:
            root = os.path.join(root, package_path)

            if os.path.isdir(root):
                schema_root = root
                break

    if schema_root is None:
        raise ValueError(
            f"The {package_name!r} package was not installed in a"
            " way that PackageLoader understands."
        )

    return schema_root


def get_default_loader(package_name: str) -> DefaultLoader:
    return DefaultLoader(get_schema_root(package_name))
