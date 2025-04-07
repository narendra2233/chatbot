input_prompt = """
      Examine the financial performance data in the provided below context_data and suggest a title that best represents the financial health and trends and generate insights by following below rules. 

      Make use of the Column definitions from raw data below while generating insights.
      Column definitions are defined in column_context below.

      <column_context>
      {column_context}
      </column_context>

      Feedback data is provided below in context_feedback.
      
      Feedback data contains outputs of similar examples with score. Here score is equal to 0 means the summary is very bad and score is equal to 1 means summary is very good.
      Please analyze the feedback data containing summary and score and try to generate response similar to summary whose score is equal to 1.
      Please avoid generating the response similar to summary whose score is 0.
      You are provided with feedback data so that you can get an idea about what an generated response look like and not look like also based on score given.

      <context_feedback>
      {context_feedback}
      </context_feedback>

      Data is provided below in context_data.
      
      Provide your insights by analysisg the data which can be comparative analysis for year over year/ quarter over quarter, comparisons from peers or likewise.
      Please analyze the data and generate 4 insights based on the given rules.
      
      Rules:
      1. Examine the Country-wise data in the dataframe for each country by Sum of trx which is sum of transactions and Sum of pv_usd which is sum of amount in US Dollars. Suggest a title that best represents the financial health and main trends.
      2. Always keep the title first and then the rest insights should follow.
      3. Generate insights of at least 30 to maximum 35 words each.
      4. Summarize the data and provide numerical data points all under 30 to 40 words and it should be verbal and complete sentance.
      5. Use finance vocabulary to provide precise insights.
      6. Avoid vague sentences; start with specific observations.
      7. Provide clear and concise analysis for each data point.
      8. Each insight should be meaningful and add value to the overall analysis.
      9. Title can be a maximum of 10 words.
      10. Use finance-related jargon relevant to the data.
      11. Avoid using generic terms; be specific about the metrics or trends.
      12. The title should use relevant finance jargon.
      13. The title should clearly reflect the data content.
      14. Provide numerical data also in the insights by refering to the original data.
      15. Feel free to convert decimal data to percentage where it is necessary by judging the nature of the metric.
      16. Do not display wrong numerical values or wrong data.
      18. If you get metric_type equal to trx then shows values as credit transactions, debit transactions etc.
      19. If you get metric_type equal to pvl then shows values as credit PV Local Currency, debit PV Local currency etc.
      20. If you get metric_type equal to pvu then shows values as credit PV USD, debit PV USD etc. If you get metric_type equal to pvc then shows values as credit PV USD Constant, debit PV USD Constant etc.
      21. Average_ticket is defined as total payment volume divided by total transactions count. It is defined in average ticket size.
      22. While producing the title and insight, please look on the data type of metric and avergae ticket data.
      23. Please check the type of metric_value from metric_type and average ticket from the above definition, then generate insight and include the data unit and value details carefully.
      24. Please keep in mind while writing about data label such as Transaction count, PV local currency, PV USD, PV USD constant defined in metrci_type and average ticket.
      25. First identify the data label type from the metric_type then generate title and insight according to that.
      26. In title section, add the word from the metric_type of metric_value and avergae ticket data. 
      27. If there is no data available then generate there is no nay data available.
      28. Make the insights more prescriptive in nature and not just descriptive, like an increase in card holders in percentage terms quarter over quarter signifies good marketing campaign and same can be replicated for the rest of the areas not performing upto the mark.
      29. Do not get the data wrong at any cost.
      30. While generating answer, keep output format as 'Title: "Title content",'1. generated insights', '2. generated insights' and so on.
      31. Understand the unit from unit_of_measure such as K, M, B and T and add into the data label also.
      32. Add metric_type label as Transaction count for trx, PV Local Currency for pvl, PV USD for pvu and PV USD Constant for pvc in group by fields. Do not add staright forward transaction only. Add the label using metric_type as defined above.
  
      
      Error Cleaning-
      1. Removes the extra lines and tabs and one insight should come in one line with out leaving any lines blank.
      2. Remove word "Title" in title line and dont use 1. or 2. in title line.
      3. Remove any words Attached to insights like "Insights:", "-".
      4. Title should not be in double quotes.
      
      Stricktly follow the Rules and Generate the title and insights based on these rules, and do not make the above miskates and perform the error cleaning.


      <context_data>
      {context_data}
      </context_data>

      Questions: {input}
      
      """