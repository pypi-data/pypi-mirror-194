`sealedsecret`: A tool to manage [SealedSecrets](https://github.com/bitnami-labs/sealed-secrets)

## Installation

`pip install sealedsecretmgr`

## Usage

To list existing SealedSecrets with keys in your namespace:

```
$ sealedsecret list
my-super-secret
	DATABASE_PASSWORD
```

You can pass an optional `--namespace` or `-n` argument before any command:
```
$ sealedsecret -n dev list
my-super-secret
	DATABASE_PASSWORD
```

To retrieve and view a SealedSecret you can get it.

```
sealedsecret get secret-name
```

To create a new SealedSecret:
```
sealedsecret create new-secret-name my-key my-value-to-protect
```

To update a SealedSecret file on disk, you can use the `--merge-into` flag of the create command:

```
sealedsecret create my-super-secret DATABASE_PASSWORD new-value
```

You can use this command to add new keys or edit existing keys.

To add a key or edit an existing key in an exitsing SealedSecret:
```
sealedsecret update existing-secret-name my-new-key a-value
```

The update and create commands only print the resource, you can redirect the output of edit an update to a file and then apply it using `kubectl apply -f` or you can pipe directly to `kubectl apply -`. You can use the global argument `-o` to choose between JSON or the default YAML output.

``
sealedsecret -o json create a-secret a-key a-value
```
