const f1 = document.getElementById("image")
const f2 = document.getElementById("description")
const post = document.querySelectorAll(".post")
const dots = document.querySelectorAll(".dots")
const btns_container = document.querySelectorAll(".delUp")
const btns = document.getElementsByClassName("del-a")
const img = document.querySelectorAll(".rounded")
const space = document.getElementById("dash")

window.onload = () => {
    f1.value = ""
    f2.value = ""
    f1.setAttribute("autocomplete", "off");
    f2.setAttribute("autocomplete", "off");
}

dots.forEach( d => {
    d.addEventListener("click", () => {
        dots.forEach(d => {
            d.style.display = "none"
        })
        btns_container.forEach((btn)  => {
            btn.style.display = "block"
        })
    })
})

post.forEach(p => {
    p.addEventListener("mouseleave", ()=> {
        btns_container.forEach(b => {
            b.style.display = "none"
        })
        dots.forEach(d => {
            d.style.display = "flex"
        })
    })
})

img.forEach( (image, index) => {
    image.addEventListener("click", ()=> {  
        console.log("click" + index)
        image_preview(image.src)
    })
})

const image_preview = (img) => {
    const d = document.createElement("div")
    const th = document.createElement("img")
    const exit = document.createElement("h1")

    th.src = img
    d.classList.add("viewImage")
    exit.innerText = "X"
    d.appendChild(exit)
    d.appendChild(th)

    exit.addEventListener('click', ()=> {
        d.style.display = "none"
    })

    return space.appendChild(d)

}

