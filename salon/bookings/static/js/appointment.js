function stopClick(event) {
    event.stopPropagation()
}

function make_appointment(event) {
    console.log(event.currentTarget)
    // event.target - на кого и правда нажали
    // event.currentTarget - кто перехватил событие на этапе всплытия
    let li = event.currentTarget  // Элемент списка, содержащий кнопку, которую мы нажали
    console.log(li.querySelector('[type=hidden]'))  // Скрытый инпут, принадлежащий элементу списка
    let s = li.querySelector('select')
    console.log(s)
    if (s.style.display == 'block') {
        let start_dt = li.querySelector('[type=hidden]').value
        let end_dt = ''
        let master_id = s.value
        ask_server_make_appointement(master_id, start_dt, end_dt)
    } else {
        s.style.display = 'block'
    }
}

function ask_server_make_appointement(master_id, start_dt, end_dt) {
    fetch('/book_from_calendar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
            master_id: master_id,
            start_dt: start_dt,
            end_dt: end_dt,
        })
    })
}