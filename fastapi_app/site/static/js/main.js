try {
    tg = window.Telegram.WebApp;
    tg.expand();
} catch (e) {
    alert("Telegram Error: " + e);
}


window.onload = function () {
    const currentUrl = window.location.href.split('/');
    const nameHTMLFile = (currentUrl[currentUrl.length - 1]).split('?')[0];
    if (nameHTMLFile === 'index' || nameHTMLFile.length < 2) {
        setActiveButton('profile_button');
    }else if (nameHTMLFile === 'settings') {
        setActiveButton('settings_button');
    } else if (nameHTMLFile === 'slaves') {
        setActiveButton('slaves_button');
        createSlaveItems().then(r => console.log(r));
    } else if (nameHTMLFile === 'top_players') {
        setActiveButton('top_players_button');
    }
}

function setActiveButton(activeButton) {
    const buttons = document.querySelectorAll('.nav__button');
    buttons.forEach(button => {
        button.classList.remove('active');
    });
    document.getElementById(activeButton).classList.add('active');
}


async function createSlaveItems() {
    const container = document.querySelector('.slaves__container'); // Убедитесь, что контейнер существует
    let slaves = await GetSlaves();
    for (let slave of slaves) {
        const slaveItem = document.createElement('div');
        slaveItem.className = 'slave__item';
        slaveItem.innerHTML = `
            <button class="slave__avatar__button">
                <img class="slave__avatar__image" src="${slave.photo_url}" alt="">
            </button>
            <div class="slave__nickname">
                ${slave.first_name}
            </div>
            <div class="slave__action__buttons">
            <div class="slave__improve">
                <button class="slave__improve__button">
                    <img class="slave__improve__image" src="/static/images/slaves_container/improve.png" alt="">
                </button>
                <div class="slave__improve__text">Улучшить</div>
            </div>
            <div class="slave__block">
                <button class="slave__block__button">
                    <img class="slave__block__image" src="/static/images/slaves_container/block.png" alt="">
                </button>
                <div class="slave__block__text">Оковы</div>
            </div>
            <div class="slave__sell">
                <button class="slave__sell__button">
                    <img class="slave__sell__image" src="/static/images/slaves_container/sell.png" alt="">
                </button>
                <div class="slave__sell__text">Продать</div>
            </div>
                
            </div>
        `;

        container.appendChild(slaveItem);
    }
}



async function setProfile() {
    try {
        const user = tg.initDataUnsafe.user;
        document.getElementById("profile_image").src = user.photo_url;
        document.getElementById('profile_name').innerText = user.username;
        document.getElementById('profile_user_id').innerText = 'ID: ' + user.id;
        document.getElementById('date_registration').innerText = getNowDate();
        await sendUserData(user);
    } catch (e) {
        alert(e);
    }

}
PUBLIC_URL = 'https://decently-pioneering-tilefish.cloudpub.ru'
async function sendUserData(user) {
    const item = {user_id: user.id,
        username: user.username ?? 'None',
        first_name: user.first_name ?? 'None',
        last_name: user.last_name ?? 'None',
        is_premium: user.is_premium ?? false,
        photo_url: user.photo_url ?? 'None'
    };

    const response = await fetch(PUBLIC_URL + '/check_user/', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(item)});
    const data = await response.json();
    if (data.success) {
        await logging(`Пользователь ${data.username} | ${data.user_id} успешно добавлен`)
    }
    else {
        await logging(`Пользователь  ${data.username} | ${data.user_id} ошибка добавления`)
    }

}

async function logging(data) {
    const log = {data: data};
    const response = await fetch(PUBLIC_URL + '/logs/', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(log)});
}

function getNowDate() {
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0'); // Получаем день и добавляем ведущий ноль
    const month = String(today.getMonth() + 1).padStart(2, '0'); // Получаем месяц (0-11) и добавляем 1, затем ведущий ноль
    const year = today.getFullYear(); // Получаем год

    return `${day}.${month}.${year}`;
}

async function getInviteURL() {
    const user = tg.initDataUnsafe.user;
    const response = await fetch(`${PUBLIC_URL}/invite_link/?user_id=${user.id}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
    const data = await response.json();
    if (data.success === 1) {
        await logging(`Пользователь ${user.username} | ${user.id} успешно получил пригласительную ссылку: ${data.invite_link}`)
        return data.invite_link;
    } else if (data.success === 0) {
        await logging(`Пользователь  ${user.username} | ${user.id} не получил ссылку ${data.error}`)
        return null;
    }
}

async function CopyLinkOnClick() {
    const link = await getInviteURL();
    navigator.clipboard.writeText(link).then(() => {
        alert('Пригласительная ссылка скопирована в буфер обмена!');
    }).catch(err => {
        document.getElementById('link_value').value = link;
        document.getElementById('popup_link').style.display = 'flex';

    });


}
async function ClosePopupLink() {
    document.getElementById('popup_link').style.display = 'none';
}

async function GetSlaves(){
    const user = tg.initDataUnsafe.user;
    const response = await fetch(`${PUBLIC_URL}/get_slaves/?user_id=${user.id}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
    const data = await response.json();
    if (data.success) {
        await logging(`Пользователь ${user.username} | ${user.id} успешно получил список рабов`)
        return data.slaves
    } else  {
        await logging(`Пользователь  ${user.username} | ${user.id} не получил список рабов ${data.error}`)
        return null;
    }
}