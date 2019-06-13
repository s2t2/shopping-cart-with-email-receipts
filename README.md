# Shopping Cart Project Solution

... with functionality for sending a receipt via email.

## Installation

Fork [this repo](https://github.com/s2t2/shopping-cart-with-email-receipts), then clone your fork to download it locally onto your computer. Then navigate there from the command-line:

```sh
cd shopping-cart-with-email-receipts
```

## Setup

### Credentials Setup

Follow [this tutorial](https://github.com/prof-rossetti/nyu-info-2335-201905/blob/master/notes/python/packages/sendgrid.md) to sign up for a Sendgrid API Key and configure your own Sendgrid Email Template, then locate the template's unique identifier.

Create a new file called ".env" in the root directory of this repo, then copy the contents of the "env.example" file into it. Then adapt the values in the ".env" file to specify your own `SENDGRID_API_KEY`,
`SENDGRID_TEMPLATE_ID`, and `EMAIL_ADDRESS` values, respectively.

### Environment Setup

Setup a virtual environment called something like "emails-env" and from within it install a specific version of the `sendgrid` package, which we'll use to send the emails:

```sh
conda create emails-env python=3.7 # (first time only)
conda activate emails-env

pip install sendgrid==6.0.5
```

## Usage

Run the checkout process:

```sh
python checkout.py
```

## [License](/LICENSE.md)
