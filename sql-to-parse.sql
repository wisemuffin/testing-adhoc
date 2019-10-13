select
,"A11 Order"."order id"
,"A11 Work Order"."work order id"

, "all_exclusions" = 'N'
as "order-tf"

, "inc excl" = 'N'
and "is inc" = 'Y'
as "incident-tf"

,"order-tf"
and "incident-tf"
and "snap date" > '2019-01-01'
as "metric 1"

, "incident-tf"
as "metric2"

from cc_dde."order_t" as "A11 Order"
inner join fld_dde."work_order_t" as "A11 Work Order" on "A11 Order"."order_key" = "A11 Work Order"."order_key"