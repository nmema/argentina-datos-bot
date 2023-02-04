#!/usr/bin/env python3
import aws_cdk as cdk

from backend.component import Backend


app = cdk.App()
Backend(app, "ArgentinaConDatos")

app.synth()
