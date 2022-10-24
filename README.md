# accounting
Apps related to Odoo it's accounting features

- [auto_invoice_advance](#auto_invoice_advance): automatically generate (draft) advance invoice


## auto_invoice_advance
This module adds support for automatically generating a (draft) advance invoice for confirmed orders.<br/>
The percentage of the advance is configurable under Sales > Configuration > Settings under the block "Invoicing":
![image](https://user-images.githubusercontent.com/6352350/197563466-cc64ed2b-4714-4cb9-8a55-08e4c78b43c7.png)

Odoo automatically processes confirmed sale orders that do not yet have any invoices.<br/>
This is done with the cron job "Sale: create advance invoices" which you can find under Settings > Technical > Automation > Scheduled Actions.<br/>
By default the cron job runs once an hour.
