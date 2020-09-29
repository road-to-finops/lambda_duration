SELECT fucntionname,
         memorysize,
        "Max Memory Used",
        cast( ltrim(replace("Max Memory Used",
         'MB')) as varchar) AS "Max Memory"
FROM "athenacurcfn_mybillingreport"."lambda_usage"