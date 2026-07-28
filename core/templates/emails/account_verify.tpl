<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verify Your Email</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #f4f6f9;
            font-family: Arial, Helvetica, sans-serif;
        }

        .container {
            max-width: 600px;
            margin: 40px auto;
            background: #ffffff;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, .08);
        }

        .header {
            background: #2563eb;
            color: #fff;
            text-align: center;
            padding: 30px 20px;
        }

        .header h1 {
            margin: 0;
            font-size: 28px;
        }

        .content {
            padding: 40px 30px;
            color: #444;
            line-height: 1.8;
        }

        .content h2 {
            color: #222;
            margin-top: 0;
        }

        .button {
            display: inline-block;
            margin: 30px 0;
            padding: 14px 32px;
            background-color: #2563eb;
            color: #ffffff !important;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
        }

        .link-box {
            word-break: break-all;
            background: #f8f9fa;
            border: 1px solid #ddd;
            padding: 12px;
            border-radius: 6px;
            font-size: 14px;
            color: #555;
        }

        .footer {
            text-align: center;
            padding: 20px;
            color: #777;
            font-size: 13px;
            border-top: 1px solid #eee;
        }

        .footer a {
            color: #2563eb;
            text-decoration: none;
        }

        @media only screen and (max-width: 600px) {
            .content {
                padding: 25px;
            }

            .button {
                display: block;
                text-align: center;
            }
        }
    </style>
</head>
<body>

<div class="container">

    <div class="header">
        <h1>My Blog</h1>
    </div>

    <div class="content">

        <!--        <h2>Hello {{ first_name|default:email }},</h2>-->
        <h2>Hello Mehran,</h2>

        <p>
            Thank you for registering.
            To activate your account, please click the button below.
        </p>

        <p style="text-align:center;">
            <a href="{{ activation_link }}" class="button">
                Verify Email
            </a>
        </p>

        <p>
            If the button doesn't work, copy and paste the following link into your browser:
        </p>

        <div class="link-box">
            {{ activation_link }}
        </div>

        <p>
            This activation link will expire after a limited time.
        </p>

        <p>
            If you did not create this account, you can safely ignore this email.
        </p>

    </div>

    <div class="footer">
        © {% now "Y" %} My Blog. All rights reserved.
    </div>

</div>

</body>
</html>

