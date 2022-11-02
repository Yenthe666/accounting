# accounting
Apps related to Odoo it's accounting features

- [auto_invoice_advance](#auto_invoice_advance): automatically generate (draft) advance invoice


## auto_invoice_advance
This module adds support for automatically:
- Generating draft advance invoice(s) for confirmed sale orders,
- Automatically confirming the invoice(s) if configured,
- Automatically e-mailing the invoice(s) if configured

The app is configurable under Sales > Configuration > Settings under the block "Invoicing":
![image](https://user-images.githubusercontent.com/6352350/199924728-8bf36c62-b2d6-490e-b9bc-d05c096d8265.png)

Let's go over the configuration options:
- <b>Down payment percentage</b>: percentage of the total amount (excluding taxes) that we should create a down payment for,
- <b>Automatically confirm down payments</b>: will automatically confirm the down payments (draft invoices) if set to True, otherwise the invoices stay in draft,
- <b>Automatically send down payment email to customer</b>: will automatically email the confirmed down payment (invoice) to the customers,
- <b>Down payment email</b>: the e-mail template used to send out the down payment (invoice) e-mails to the customers

Odoo will automatically processes confirmed sale orders that do not yet have any invoices.<br/>
This is done with the cron job "Sale: create advance invoices" which you can find under Settings > Technical > Automation > Scheduled Actions.<br/>
By default the cron job runs once an hour.
