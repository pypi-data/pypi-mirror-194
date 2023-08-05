# SQuARE Datastore Client
This package facilites the interaction with datastores hosted in [UKP-SQuARE](https://square.ukp-lab.de/).

## Installation
```bash
pip install square-datastore-client
```

## Usage
After installing, Datastores in SQuARE can be called easily. Before running the code, the follinwg environment variables need to be set.
```bash
export SQUARE_API_URL=https://square.ukp-lab.de/api
export KEYCLOAK_BASE_URL=https://square.ukp-lab.de
export REALM=square
export CLIENT_ID=<INSERT>
export CLIENT_SECRET=<INSERT>
```
- `SQUARE_API_URL`: The address where the SQuARE API's are hosted. For UKP-SQuARE set this to `https://square.ukp-lab.de/api`. If you run SQuARE locally, set this to your address.
- `KEYCLOAK_BASE_URL`: The address where tokens can be obtained from. For UKP-SQuARE set this to `https://square.ukp-lab.de`
- `REALM`: The realm in which your Keycloak client resides. For UKP-SQuARE this is `square`.
- `CLIENT_ID`: The ID of your client. For UKP-SQuARE, you will receive this from the UI when creating a new skill.*
- `CLIENT_SECRET`: The secret of your client/skill. For UKP-SQuARE, you will receive this from the UI when creating a new skill.*

*) This is currently not supported in the UI. However, when you open the developer tab in your browser, you will see the response from the API containing the `CLIENT_ID` and `CLIENT_SECRET`.

```python
import asyncio

from square_datastore_client import SQuAREDatastoreClient


async def main():
    square_datastore_client = SQuAREDatastoreClient()
    
    query = "When was TU Darmstadt established?"
    data = await square_datastore_client(
        datastore_name="nq", index_name="dpr", query=query
    )
    
    context = [d["document"]["text"] for d in data]
    context_score = [d["score"] for d in data]
    for i, (c, s) in enumerate(zip(context, context_score)):
        print(f"#{i} Score={s:6.3f} Doc={c:.50}...\"")

    #0 Score=77.239 Doc="Technische Universität Darmstadt The Technische U..."
    #1 Score=76.951 Doc="Institutes of Technology in Germany which were es..."
    #2 Score=76.811 Doc="TU9 TU9 German Institutes of Technology e. V. is ..."
    #3 Score=75.621 Doc="in 1971 and is the largest University of Applied ..."
    #4 Score=75.186 Doc="TU9, a network of the most notable German ""Techn..."
    #5 Score=74.483 Doc="workers in technological subjects such as mechani..."
    #6 Score=74.355 Doc="Texas Lutheran University Texas Lutheran Universi..."
    #7 Score=73.958 Doc="founded in 1836 and received its own building nea..."
    #8 Score=73.371 Doc="Tasmania University Union The Tasmania University..."
    #9 Score=73.325 Doc="as 'Technical High School', providing a totally m..."  

# Note, the SQuAREDatastoreCLient is usually called within an endpoint that is async.
# In that case, the following line is not needed.
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

```
