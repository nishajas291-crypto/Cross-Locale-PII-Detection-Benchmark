# PII detection results (model: en_core_web_sm, 1500 sentences)

## By entity type

| detector                     | entity        |   TP |   FP |   FN |   precision | precision_ci   |   recall | recall_ci    |      f1 |
|:-----------------------------|:--------------|-----:|-----:|-----:|------------:|:---------------|---------:|:-------------|--------:|
| Presidio (default)           | CREDIT_CARD   |  176 |    2 |  106 |       0.989 | [0.96, 1.00]   |    0.624 | [0.57, 0.68] |   0.765 |
| Presidio (default)           | EMAIL_ADDRESS |  234 |    0 |    0 |       1     | [0.98, 1.00]   |    1     | [0.98, 1.00] |   1     |
| Presidio (default)           | IN_AADHAAR    |    0 |    0 |   77 |     nan     | [nan, nan]     |    0     | [0.00, 0.05] | nan     |
| Presidio (default)           | IN_PAN        |    0 |    0 |   65 |     nan     | [nan, nan]     |    0     | [0.00, 0.06] | nan     |
| Presidio (default)           | PERSON        |  381 |   17 |   64 |       0.957 | [0.93, 0.97]   |    0.856 | [0.82, 0.89] |   0.904 |
| Presidio (default)           | PHONE_NUMBER  |  232 |   41 |   29 |       0.85  | [0.80, 0.89]   |    0.889 | [0.84, 0.92] |   0.869 |
| Presidio (default)           | US_SSN        |   99 |    0 |    0 |       1     | [0.96, 1.00]   |    1     | [0.96, 1.00] |   1     |
| Presidio + India recognizers | CREDIT_CARD   |  176 |    2 |  106 |       0.989 | [0.96, 1.00]   |    0.624 | [0.57, 0.68] |   0.765 |
| Presidio + India recognizers | EMAIL_ADDRESS |  234 |    0 |    0 |       1     | [0.98, 1.00]   |    1     | [0.98, 1.00] |   1     |
| Presidio + India recognizers | IN_AADHAAR    |   77 |    9 |    0 |       0.895 | [0.81, 0.94]   |    1     | [0.95, 1.00] |   0.945 |
| Presidio + India recognizers | IN_PAN        |   65 |  149 |    0 |       0.304 | [0.25, 0.37]   |    1     | [0.94, 1.00] |   0.466 |
| Presidio + India recognizers | PERSON        |  381 |   17 |   64 |       0.957 | [0.93, 0.97]   |    0.856 | [0.82, 0.89] |   0.904 |
| Presidio + India recognizers | PHONE_NUMBER  |  232 |   41 |   29 |       0.85  | [0.80, 0.89]   |    0.889 | [0.84, 0.92] |   0.869 |
| Presidio + India recognizers | US_SSN        |   99 |    0 |    0 |       1     | [0.96, 1.00]   |    1     | [0.96, 1.00] |   1     |
| Regex baseline               | CREDIT_CARD   |  282 |   59 |    0 |       0.827 | [0.78, 0.86]   |    1     | [0.99, 1.00] |   0.905 |
| Regex baseline               | EMAIL_ADDRESS |  234 |    0 |    0 |       1     | [0.98, 1.00]   |    1     | [0.98, 1.00] |   1     |
| Regex baseline               | IN_AADHAAR    |   77 |   77 |    0 |       0.5   | [0.42, 0.58]   |    1     | [0.95, 1.00] |   0.667 |
| Regex baseline               | IN_PAN        |   65 |   51 |    0 |       0.56  | [0.47, 0.65]   |    1     | [0.94, 1.00] |   0.718 |
| Regex baseline               | PERSON        |  445 |    0 |    0 |       1     | [0.99, 1.00]   |    1     | [0.99, 1.00] |   1     |
| Regex baseline               | PHONE_NUMBER  |  223 |  361 |   38 |       0.382 | [0.34, 0.42]   |    0.854 | [0.81, 0.89] |   0.528 |
| Regex baseline               | US_SSN        |   99 |    0 |    0 |       1     | [0.96, 1.00]   |    1     | [0.96, 1.00] |   1     |

## Recall by locale (US vs Indian formats)

| detector                     | locale   | entity        |   n |   recall | recall_ci    |
|:-----------------------------|:---------|:--------------|----:|---------:|:-------------|
| Presidio (default)           | IN       | CREDIT_CARD   | 137 |    0.635 | [0.55, 0.71] |
| Presidio (default)           | IN       | EMAIL_ADDRESS | 121 |    1     | [0.97, 1.00] |
| Presidio (default)           | IN       | IN_AADHAAR    |  77 |    0     | [0.00, 0.05] |
| Presidio (default)           | IN       | IN_PAN        |  65 |    0     | [0.00, 0.06] |
| Presidio (default)           | IN       | PERSON        | 218 |    0.761 | [0.70, 0.81] |
| Presidio (default)           | IN       | PHONE_NUMBER  | 118 |    1     | [0.97, 1.00] |
| Presidio (default)           | US       | CREDIT_CARD   | 145 |    0.614 | [0.53, 0.69] |
| Presidio (default)           | US       | EMAIL_ADDRESS | 113 |    1     | [0.97, 1.00] |
| Presidio (default)           | US       | PERSON        | 227 |    0.947 | [0.91, 0.97] |
| Presidio (default)           | US       | PHONE_NUMBER  | 143 |    0.797 | [0.72, 0.85] |
| Presidio (default)           | US       | US_SSN        |  99 |    1     | [0.96, 1.00] |
| Presidio + India recognizers | IN       | CREDIT_CARD   | 137 |    0.635 | [0.55, 0.71] |
| Presidio + India recognizers | IN       | EMAIL_ADDRESS | 121 |    1     | [0.97, 1.00] |
| Presidio + India recognizers | IN       | IN_AADHAAR    |  77 |    1     | [0.95, 1.00] |
| Presidio + India recognizers | IN       | IN_PAN        |  65 |    1     | [0.94, 1.00] |
| Presidio + India recognizers | IN       | PERSON        | 218 |    0.761 | [0.70, 0.81] |
| Presidio + India recognizers | IN       | PHONE_NUMBER  | 118 |    1     | [0.97, 1.00] |
| Presidio + India recognizers | US       | CREDIT_CARD   | 145 |    0.614 | [0.53, 0.69] |
| Presidio + India recognizers | US       | EMAIL_ADDRESS | 113 |    1     | [0.97, 1.00] |
| Presidio + India recognizers | US       | PERSON        | 227 |    0.947 | [0.91, 0.97] |
| Presidio + India recognizers | US       | PHONE_NUMBER  | 143 |    0.797 | [0.72, 0.85] |
| Presidio + India recognizers | US       | US_SSN        |  99 |    1     | [0.96, 1.00] |
| Regex baseline               | IN       | CREDIT_CARD   | 137 |    1     | [0.97, 1.00] |
| Regex baseline               | IN       | EMAIL_ADDRESS | 121 |    1     | [0.97, 1.00] |
| Regex baseline               | IN       | IN_AADHAAR    |  77 |    1     | [0.95, 1.00] |
| Regex baseline               | IN       | IN_PAN        |  65 |    1     | [0.94, 1.00] |
| Regex baseline               | IN       | PERSON        | 218 |    1     | [0.98, 1.00] |
| Regex baseline               | IN       | PHONE_NUMBER  | 118 |    0.678 | [0.59, 0.76] |
| Regex baseline               | US       | CREDIT_CARD   | 145 |    1     | [0.97, 1.00] |
| Regex baseline               | US       | EMAIL_ADDRESS | 113 |    1     | [0.97, 1.00] |
| Regex baseline               | US       | PERSON        | 227 |    1     | [0.98, 1.00] |
| Regex baseline               | US       | PHONE_NUMBER  | 143 |    1     | [0.97, 1.00] |
| Regex baseline               | US       | US_SSN        |  99 |    1     | [0.96, 1.00] |

## False alarms on PII-free sentences

| detector                     |   false_alarms |   pii_free_sentences | most_common                               |
|:-----------------------------|---------------:|---------------------:|:------------------------------------------|
| Regex baseline               |            235 |                  300 | IN_AADHAAR:77, CREDIT_CARD:59, IN_PAN:51  |
| Presidio (default)           |             24 |                  300 | PHONE_NUMBER:16, PERSON:6, CREDIT_CARD:2  |
| Presidio + India recognizers |            151 |                  300 | IN_PAN:118, PHONE_NUMBER:16, IN_AADHAAR:9 |
