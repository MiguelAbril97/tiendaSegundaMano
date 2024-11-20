window.addEventListener("load", inicializar);

function inicializar(){


    const enlaces = document.getElementsByTagName("a");

    for (let i = 0; i < enlaces.length; i++) {
        enlaces[i].addEventListener("mouseover", function() {
            enlaces[i].style.color = "red"; 
        });

        enlaces[i].addEventListener("mouseout", function() {
            enlaces[i].style.color = "black"; 
        });
    }
   
  
}