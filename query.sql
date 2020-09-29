SELECT *,("Provisioned Memory"- "Max Memory") As "Unutilized Memory" from
    (SELECT fucntionname,
         memorysize AS "Provisioned Memory",
         cast( trim(replace("Max Memory Used",
         'MB')) AS integer) AS "Max Memory"
    FROM "athenacurcfn_mybillingreport"."lambda_usage")