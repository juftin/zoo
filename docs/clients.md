# API Clients

```shell
hatch run generate:all
```

## Python

The python client is generated using [openapi-generator](https://openapi-generator.tech/). It will be
generated in the `dist/clients/python` directory.

```python
from typing import List, Dict, Any

from openapi_client import ApiClient, AnimalsApi, AnimalsRead, Configuration

config = Configuration(host="http://localhost:8000")
client = ApiClient(configuration=config)
animals_api = AnimalsApi(api_client=client)
animals_dicts: List[Dict[str, Any]] = animals_api.animals_get_animals()
animals = [AnimalsRead(**animal) for animal in animals_dicts]
```

## TypeScript

The TypeScript client is generated
using [openapi-typescript-codegen](https://github.com/ferdikoomen/openapi-typescript-codegen). It will be
generated in the `dist/clients/typescript` directory.

```typescript
import { AnimalsApi, AnimalsRead } from "./clients/typescript";

const animalsApi = new AnimalsApi({ basePath: "http://localhost:8000" });
const animals: AnimalsRead[] = await animalsApi.animalsGetAnimals();
```

!!! note
The TypeScript client is not yet documented :smile:
