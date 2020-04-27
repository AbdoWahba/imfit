## Installation

### Step1: Install [Node.js](https://nodejs.org/) LTS version from [here](https://nodejs.org/en/download/)

check node version by running `node -v` in you terminal then check npm version by running `npm -v`

### step2: Install yarn

run these commands:

`curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add - echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list`

then run :

`sudo apt update && sudo apt install yarn`

check if yarn is installed successfully by running :

`yarn -v`

### step3: Install create-react-native-app

run: `npm i -g create-react-native-app`

check if installed successfully: `create-react-native-app -v`

### step4: Insatll expo-cli

run: `npm i -g expo-cli`

check if installed successfully:
`expo --version`

### step5: clone [this repo](https://github.com/AbdoWahba/imfit)

`git clone https://github.com/AbdoWahba/imfit`

### step6: checkout to development branch

`git checkout --track origin/development`

### step7: run `yarn install` inside project dir

### step8: Install [expo android client](https://play.google.com/store/apps/details?id=host.exp.exponent&hl=en) on you android mobil

### step9: run `yarn start` inside project dir

### step10: open expo android client and read QR code on loclhost [port 19002](http://localhost:19002/)
