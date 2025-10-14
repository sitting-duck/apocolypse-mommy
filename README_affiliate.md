
<img width="852" height="697" alt="image" src="https://github.com/user-attachments/assets/fc1e50e8-1050-43dc-861f-1476368c2e0f" /> <br>

You will need to create a public Telegram channel to use for the website Amazon is asking for in the image above. <br>

To create a Telegram channel, open Telegram and tap the "New Message" icon, then select "New Channel". <br>
<img width="514" height="258" alt="image" src="https://github.com/user-attachments/assets/235a8ff2-344c-400f-88aa-405296a2ad8e" /> <br>

Click the create button <br>
<img width="391" height="640" alt="image" src="https://github.com/user-attachments/assets/e8e1b793-a7ed-4ed1-89dd-a9a6c372c8eb" />

Make sure you set the channel to public and git it a url. <br>
<img width="380" height="624" alt="image" src="https://github.com/user-attachments/assets/92a26859-f727-4568-b12e-d6fd9bdd3182" /> <br>


You will be prompted to give your channel a name, description, and an icon. Finally, choose between a public or private channel and add initial contacts before completing the setup. <br>
<img width="388" height="634" alt="image" src="https://github.com/user-attachments/assets/f8889a5b-77b0-47e2-8114-0bc805463a6c" /> <br>

Now copy the url and paste it into the web field on the Amazon Affiliates page. <br>
`https://t.me/apocolypse_meow`<br>

<img width="825" height="495" alt="image" src="https://github.com/user-attachments/assets/fa201853-d7b4-47ac-8d0c-63cb15c931b6" /> <br>

Fill out the form. 
<img width="809" height="769" alt="image" src="https://github.com/user-attachments/assets/f34cae95-a05d-49c6-bfa3-d89ae4d724dd" /> <br>


Success page <br>
<img width="797" height="443" alt="image" src="https://github.com/user-attachments/assets/053c605e-c7e6-44ea-a6dc-a6a2a4d631ee" /><br>

### Potential Delay
<img width="914" height="342" alt="image" src="https://github.com/user-attachments/assets/00e810a8-ccc9-4372-97e1-944ae3315b13" /> <br>

to get the API key for pulling affiliate links in code, you need to first have 3 purchases using affiliate links from your account that you created manually. <br>
Once your Amazon account has completed the initial affiliate set up process, you will see a banner like this while shopping on Amazon normally <br>
<img width="1446" height="78" alt="image" src="https://github.com/user-attachments/assets/d592851e-b272-4dc1-bd5f-08609051a933" /> <br>


# amazon secrets
go to https://affiliate-program.amazon.com/assoc_credentials/home


### setup environment variables
```bash
export PAAPI_ACCESS_KEY="AKIAxxxxxxxxxxxxxxxx"
export PAAPI_SECRET_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export PAAPI_PARTNER_TAG="apocalypseprep-20"     # your Associate tag
export PAAPI_MARKETPLACE="www.amazon.com"        # US marketplace

# helper: add or update a line like: export KEY="VALUE"
add_or_update() {
  KEY="$1"; VAL="$2"
  if grep -q "^export ${KEY}=" ~/.zshrc; then
    # macOS sed needs the empty '' arg
    sed -i '' "s|^export ${KEY}=.*$|export ${KEY}=\"${VAL//\\/\\\\}\"|" ~/.zshrc
  else
    echo "export ${KEY}=\"${VAL}\"" >> ~/.zshrc
  fi
}

add_or_update PAAPI_ACCESS_KEY   "AKIAxxxxxxxxxxxxxxxx"
add_or_update PAAPI_SECRET_KEY   "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
add_or_update PAAPI_PARTNER_TAG  "apocalypseprep-20"
add_or_update PAAPI_MARKETPLACE  "www.amazon.com"

# reload zsh so the vars are available in new commands
exec zsh   # or: source ~/.zshrc

echo "$PAAPI_ACCESS_KEY" "$PAAPI_PARTNER_TAG" "$PAAPI_MARKETPLACE"

gh secret set PAAPI_ACCESS_KEY  -b"$PAAPI_ACCESS_KEY"
gh secret set PAAPI_SECRET_KEY  -b"$PAAPI_SECRET_KEY"
gh secret set PAAPI_PARTNER_TAG -b"$PAAPI_PARTNER_TAG"
gh secret set PAAPI_MARKETPLACE -b"$PAAPI_MARKETPLACE"

```

### sttart coding
```bash

pip install python-amazon-paapi

```

### Success
<img width="387" height="629" alt="image" src="https://github.com/user-attachments/assets/6f856af5-8c20-4080-98e2-38ed2bff9e2d" />






