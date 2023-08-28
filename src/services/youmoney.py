from yoomoney import Authorize

Authorize(
      client_id="A898DA3BCA47E9EE015F9687F7657DEA1AE92D64D17A7001B2D0B05225FC4002",
      redirect_uri="https://t.me/piro_sahalin_bot",
      scope=["account-info",
             "operation-history",
             "operation-details",
             "incoming-transfers",
             "payment-p2p",
             "payment-shop",
             ]
      )