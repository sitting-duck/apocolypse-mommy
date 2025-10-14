dev:	  ## Run app
	./scripts/run_app.sh
ngrok:    ## Start ngrok
	./scripts/run_ngrok.sh
hook:     ## Register webhook to current ngrok https URL
	./scripts/register_webhook.sh
unhook:   ## Delete webhook
	./scripts/unregister_webhook.sh

