# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.ext import google
from cbra.ext.oauth2 import AuthorizationEndpoint


app = google.Service(docs_url='/ui')
app.add(AuthorizationEndpoint, path='/oauth2/authorize')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('__main__:app', reload=True) # type: ignore
