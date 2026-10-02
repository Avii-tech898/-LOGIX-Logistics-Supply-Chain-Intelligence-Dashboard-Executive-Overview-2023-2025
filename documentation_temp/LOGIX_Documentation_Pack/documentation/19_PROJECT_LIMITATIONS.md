# Project Limitations

1. LOGIX uses synthetic data rather than real company operational data.
2. Vehicle-level shipment performance cannot be derived from the current shipment schema because `vehicle_id` is not present.
3. Driver-level shipment performance has the same limitation.
4. SLA metric semantics require a final review of the denominator and delivered-shipment definition.
5. Power BI Executive Overview is currently partially completed and intentionally on hold.
6. ML models are an advanced layer and should not be represented as production models until trained and evaluated.
7. Streamlit is currently a local analytics dashboard unless a deployment is separately completed.
