# Copyright 2018-2021
# Institute of Neuroscience and Medicine (INM-1), Forschungszentrum Jülich GmbH

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from .requests import MultiSourcedRequest, GitlabProxy, GitlabProxyEnum

import re
from typing import Union, List
from abc import ABC, abstractproperty

try:
    from typing import TypedDict
except ImportError:
    # support python 3.7
    from typing_extensions import TypedDict


class EbrainsDatasetUrl(TypedDict):
    url: str


EbrainsDatasetPerson = TypedDict('EbrainsDatasetPerson', {
    '@id': str,
    'schema.org/shortName': str,
    'identifier': str,
    'shortName': str,
    'name': str
})

EbrainsDatasetEmbargoStatus = TypedDict('EbrainsDatasetEmbargoStatus', {
    "@id": str,
    'name': str,
    'identifier': List[str]
})

class EbrainsBaseDataset(ABC):
    
    @abstractproperty
    def id(self) -> str:
        raise NotImplementedError
    
    @abstractproperty
    def name(self) -> str:
        raise NotImplementedError
    
    @abstractproperty
    def urls(self) -> List[EbrainsDatasetUrl]:
        raise NotImplementedError

    @abstractproperty
    def description(self) -> str:
        raise NotImplementedError

    @abstractproperty
    def contributors(self) -> List[EbrainsDatasetPerson]:
        raise NotImplementedError

    @abstractproperty
    def ebrains_page(self) -> str:
        raise NotImplementedError

    @abstractproperty
    def custodians(self) -> EbrainsDatasetPerson:
        raise NotImplementedError
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, o: object) -> bool:
        return hasattr(o, "id") and self.id == o.id
    
    def match(self, spec: Union[str, 'EbrainsBaseDataset']) -> bool:
        """
        Checks if the given specification describes this dataset.

        Parameters
        ----------
        spec (str, EbrainsBaseDataset)
            specification to be matched.
        Returns
        -------
        bool
        """
        if spec is self:
            return True
        if isinstance(spec, str):
            return self.id == spec
        raise RuntimeError(f"Cannot match {spec.__class__}, must be either str or EbrainsBaseDataset")

class EbrainsDataset(EbrainsBaseDataset):

    def __init__(self, id, name=None, embargo_status: List[EbrainsDatasetEmbargoStatus] = None, *, cached_data=None):
        super().__init__()

        self._id = id
        self._name = name
        self._cached_data = cached_data
        self.embargo_status = embargo_status

        if id is None:
            raise TypeError("Dataset id is required")

        match = re.search(r"([a-f0-9-]+)$", id)
        if not match:
            raise ValueError(
                f"{self.__class__.__name__} initialized with invalid id: {self.id}"
            )

    @property
    def id(self) -> str:
        return self._id

    @property
    def detail(self):
        if not self._cached_data:
            match = re.search(r"([a-f0-9-]+)$", self.id)
            instance_id = match.group(1)
            self._cached_data = MultiSourcedRequest(
                requests=[
                    GitlabProxy(
                        GitlabProxyEnum.DATASET_V1,
                        instance_id=instance_id,
                    ),
                ]
            ).data
        return self._cached_data

    @property
    def name(self) -> str:
        if self._name is None:
            self._name = self.detail.get("name")
        return self._name

    @property
    def urls(self) -> List[EbrainsDatasetUrl]:
        return [
            {
                "url": f if f.startswith("http") else f"https://doi.org/{f}",
            }
            for f in self.detail.get("kgReference", [])
        ]

    @property
    def description(self) -> str:
        return self.detail.get("description")

    @property
    def contributors(self) -> List[EbrainsDatasetPerson]:
        return self.detail.get("contributors")

    @property
    def ebrains_page(self):
        return f"https://search.kg.ebrains.eu/instances/{self.id}"

    @property
    def custodians(self) -> EbrainsDatasetPerson:
        return self.detail.get("custodians")

class EbrainsV3Dataset(EbrainsBaseDataset):
    # TODO finish implementing me
    # some fields are currently missing, e.g. desc, contributors etc.
    def __init__(self, id, *, cached_data) -> None:
        super().__init__()

        self._id = id
        self._cached_data = cached_data
    
    @property
    def detail(self):
        if not self._cached_data:
            match = re.search(r"([a-f0-9-]+)$", self.id)
            instance_id = match.group(1)
            self._cached_data = MultiSourcedRequest(
                requests=[
                    GitlabProxy(
                        GitlabProxyEnum.DATASET_V3,
                        instance_id=instance_id,
                    ),
                ]
            ).data
        return self._cached_data
