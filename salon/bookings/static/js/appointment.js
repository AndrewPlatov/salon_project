function make_appointment(event) {
    console.log(event.currentTarget)
    // event.target - на кого и правда нажали
    // event.currentTarget - кто перехватил событие на этапе всплытия
    let li = event.currentTarget
    console.log(li.querySelector('[type=hidden]'))
}