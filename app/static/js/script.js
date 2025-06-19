const slides=document.querySelectorAll(".category");
let counter=0;
slides.forEach(
    (slide,index)=>{
        const width=slide.offsetWidth
        slide.style.left=  `${index*(20+width)}px `
    }
)
const goPrev=()=>{
    if(counter>0){
        counter--
        slideImage()
    }
   
}
const goNext=()=>{
    if (counter<slides.length){
        counter++
        slideImage()
    }else{counter=-1}
    
}
const slideImage= ()=>{
    slides.forEach(
        (slide)=>{
            slide.style.transform=`translateX(-${counter*115}%)`
        }
    )
}

//Creating Dropdown for expanses

const dropDownShow=( id )=>{
    let container=document.getElementById(`${id}`)
    if (!container.classList.contains('show')){
        container.classList.add('show')     
    }else{
        container.classList.remove('show')
    }
    
}