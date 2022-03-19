const modal = document.querySelector(".m");
const previews = document.querySelectorAll(".card-body img")
const original = document.querySelector(".full-img")
const caption = document.querySelector(".caption")

previews.forEach(pr => {
    pr.addEventListener("click", ()=> {
        modal.classList.add("open")
        original.classList.add("open")
        var imgSrc = pr.src
        original.src = imgSrc
        caption.textContent = pr.alt
    })
})

modal.addEventListener("click", (e)=>{
    if(e.target.classList.contains("m")) {
        modal.classList.remove("open")
        original.classList.remove("open")
    }
})
