# remote-execution

The purpose of this tool is to help with the following three use cases:

1. You want to run a piece of code in a remote environment, but the code is too large or it is otherwise impractical to paste it **into** the console (sometimes pasting many lines of code breaks the session).

2. You want to pull information from a remote environment's console, but this information is too large to easily copy it **from** the console.

3. You want to do both 1 and 2 at the same time.

## ⚠️⚠️⚠️ WARNING ⚠️⚠️⚠️
**This is not meant to be used in a production environment!**

## Dependencies

You only need `Python 3.6+` and `ngrok`. As a reminder, `ngrok` can be installed via `brew install ngrok`, and you need to configure it. Here's a sample configuration for `ngrok`. It only takes one file:

```yaml
# In mac: ~/Library/Application Support/ngrok/ngrok.yml
authtoken: "*****" # from https://dashboard.ngrok.com/get-started/your-authtoken
version: "2"
region: us
```

## Use case 1

1. Put the code that you want to run in a file. Name the file something that starts with `code` (e.g. `code.rb`, `code_pull_assignments.rb`), and place it in this directory. For example:

    ```ruby
    # code.rb
    class RemoteExecution
      def self.run
        # ... logic to run
      end
    end
    ```

1. Open a terminal session and start the `remote-execution` server with:

    ```shell
    python server.py
    ```

1. Open another terminal session and run `ngrok`:

    ```shell
    ngrok http 8000
    ```

    Take note of the `https` url as it is going to be used in the next step. This url looks something like `https://c7fd6475f29d.ngrok.io`. You could also specify the `--hostname` flag if you have one [here](https://dashboard.ngrok.com/cloud-edge/domains), but beaware that this could pose a security risk if others know this url, as they can easily see all files in this directory.

    You need to specify `8000` because `server.py` runs on that port by default.

1. Open another terminal session to console into the desired environment, and `eval` the code from step 1 by pulling it via the `ngrok` url from step 2 and using the file name for the path. For example, if you're using `ruby`:

    ```ruby
    eval(open('https://c7fd6475f29d.ngrok.io/code.rb').read); RemoteExecution.run
    eval(open('https://c7fd6475f29d.ngrok.io/code_pull_assignments.rb').read); RemoteExecution.run
    ```

That's it. If you want to test this locally, you can skip the `ngrok` step and just use `http://127.0.0.1:8000` in step 4.

## Use case 2

1. Open a terminal session and start the `remote-execution` server. See step from [Use case 1](#use-case-1) for details.

1. Open another terminal session and run `ngrok`. See step from [Use case 1](#use-case-1) for details.

1. Open another terminal session to console into the desired environment. Perform an `HTTP POST` request to the url from step 2 with the json-formatted information that you want to pull as the body of the request. For example, if you're on ruby:

    ```ruby
    payload = {'data': 5} # information that you would like to pull
    HTTParty.post('https://c7fd6475f29d.ngrok.io', :body => payload.to_json)
    ```

    You can also test this directly from curl:

    ```ruby
    curl -X POST https://c7fd6475f29d.ngrok.io -d '{"data": 6}'
    ```

## Use case 3

1. Put the code that you want to run in a file. Name the file something that starts with `code` (e.g. `code.rb`, `code_pull_assignments.rb`), and place it in this directory. Include a request at the end of the code to send the information back. If you're running ruby code, this would look something like this:

    ```ruby
    # code.rb
    class RemoteExecution
      def self.run
        payload = {} # information that you would like to pull

        # ... run code to populate `payload`

        HTTParty.post('https://c7fd6475f29d.ngrok.io', :body => payload.to_json)
      end
    end
    ```

1. Open a terminal session and start the `remote-execution` server. See step from [Use case 1](#use-case-1) for details.

1. Open another terminal session and run `ngrok`. See step from [Use case 1](#use-case-1) for details.

1. Open another terminal session to console into the desired environment, and `eval` the code from step 1 by pulling it via the `ngrok` url from step 2 and using the file name for the path. For example, if you're using `ruby`:

    ```ruby
    eval(open('https://c7fd6475f29d.ngrok.io/code.rb').read); RemoteExecution.run
    ```
