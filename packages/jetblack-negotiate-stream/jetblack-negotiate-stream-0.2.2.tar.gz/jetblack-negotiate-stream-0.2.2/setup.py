# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jetblack_negotiate_stream']

package_data = \
{'': ['*']}

install_requires = \
['pyspnego>=0.7,<0.8']

setup_kwargs = {
    'name': 'jetblack-negotiate-stream',
    'version': '0.2.2',
    'description': 'A python client for .Net NegotiateStream',
    'long_description': '# jetblack-negotiate-stream\n\nA Python client for .Net\n[NegotiateStream](https://learn.microsoft.com/en-us/dotnet/api/system.net.security.negotiatestream).\nIt supports single sign on (SSO) and encryption.\n\nThis was tested using Python 3.8 on Windows 11.\n\n## Installation\n\nInstall from pypi.\n\n```bash\npip install jetblack-negotiate-stream\n```\n\n## Example\n\nThe following programs provide a simple echo server in C# and client in Python.\n\n### Client\n\nThis is an example of a Python client using the synchronous\n`NegotiateStream` class. Note the call to `authenticate_as_client` before\nreading and writing.\n\n```python\nimport socket\n\nfrom jetblack_negotiate_stream import NegotiateStream\n\ndef main():\n    hostname = socket.gethostname()\n    port = 8181\n\n    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:\n        sock.connect((hostname, port))\n\n        stream = NegotiateStream(hostname, sock)\n\n        # Do the client side negotiate handshake.\n        stream.authenticate_as_client()\n\n        for data in (b\'first line\', b\'second line\', b\'third line\'):\n            # All reads and writes are encrypted.\n            stream.write(data)\n            response = stream.read()\n            print("Received: ", response)\n\nif __name__ == \'__main__\':\n    main()\n```\n\n### Async Client\n\nThis program uses `NegotiateStreamAsync` which is simply an asynchronous\nversion of the `NegotiateStream` class demonstrated above.\n\n```python\nimport asyncio\nimport socket\n\nfrom jetblack_negotiate_stream import NegotiateStreamAsync\n\nasync def main():\n    hostname = socket.gethostname()\n    port = 8181\n\n    reader, writer = await asyncio.open_connection(hostname, port)\n\n    stream = NegotiateStreamAsync(hostname, reader, writer)\n\n    await stream.authenticate_as_client()\n    for data in (b\'first line\', b\'second line\', b\'third line\'):\n        stream.write(data)\n        await stream.drain()\n        response = await stream.read()\n        print("Received: ", response)\n\n    stream.close()\n    await stream.wait_closed()\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n```\n\n### Alternative Async Client\n\nThe following client follows the patterns demonstrated in the asyncio library\nusing `open_negotiate_stream`. This follows the conventions of the asyncio\n`open_connection` function. The negotiation happens before the function\nreturns, resulting in cleaner code. \n\n```python\nimport asyncio\nimport socket\n\nfrom jetblack_negotiate_stream import open_negotiate_stream\n\nasync def main():\n    hostname = socket.gethostname()\n    port = 8181\n\n    # Following the same pattern as asyncio.open_connection.\n    reader, writer = await open_negotiate_stream(hostname, port)\n\n    for data in (b\'first line\', b\'second line\', b\'third line\'):\n        writer.write(data)\n        await writer.drain()\n        response = await reader.read()\n        print("Received: ", response)\n\n    writer.close()\n    await writer.wait_closed()\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n```\n\n### Server\n\nHere is a trivial C# echo server for the clients.\n\n```csharp\nusing System;\nusing System.Net;\nusing System.Net.Security;\nusing System.Net.Sockets;\nusing System.Text;\n\nnamespace NegotiateStreamServer\n{\n    internal class Program\n    {\n        static void Main(string[] args)\n        {\n            var listener = new TcpListener(IPAddress.Any, 8181);\n            listener.Start();\n\n            while (true)\n            {\n                Console.WriteLine("Listening ...");\n                var client = listener.AcceptTcpClient();\n\n                try\n                {\n                    Console.WriteLine("... Client connected.");\n\n                    Console.WriteLine("Authenticating...");\n                    var stream = new NegotiateStream(client.GetStream(), false);\n                    stream.AuthenticateAsServer();\n\n                    Console.WriteLine(\n                        "... {0} authenticated using {1}",\n                        stream.RemoteIdentity.Name,\n                        stream.RemoteIdentity.AuthenticationType);\n\n                    var buf = new byte[4096];\n                    for (var i = 0; i < 3; ++i)\n                    {\n                        var bytesRead = stream.Read(buf, 0, buf.Length);\n                        var message = Encoding.UTF8.GetString(buf, 0, bytesRead);\n                        Console.WriteLine(message);\n                        stream.Write(buf, 0, bytesRead);\n                    }\n                    stream.Close();\n                }\n                catch (Exception ex)\n                {\n                    Console.WriteLine(ex.ToString());\n                }\n            }\n        }\n    }\n}\n```\n\n## Acknowledgements\n\nThe library uses the [pyspnego](https://github.com/jborean93/pyspnego) library,\nand takes many ideas from [net.tcp-proxy](https://github.com/ernw/net.tcp-proxy).\n',
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/jetblack-negotiate-stream',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
