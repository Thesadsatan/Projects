const reviewQuoteText = document.querySelector("#review-quote-text");
const navContainer    = document.querySelector(".nav-container");
const copyBtn         = document.querySelector(".copy-btn");
const hrLine          = document.querySelector(".hr-line"); 
const quote           = document.querySelector(".random-quote");
const author          = document.querySelector("#author");
const grQuoteAddToDb  = document.querySelector('#add-to-db');
const grQuote         = document.querySelector("#gr-quote");
const grAuthor        = document.querySelector("#gr-author");
const generateBtn     = document.querySelector("#generate-btn");
const menu            = document.querySelector('#menu');
const menuLinks       = document.querySelectorAll('.link');


menu.addEventListener('click', () =>{
    if (menu.classList.contains("active")) {
        gsap.to(".links", {x: "100%"});
        gsap.set("body", {overflow: "auto"});
    }else{
        gsap.to(".links", {x: "0%"});
        gsap.to('#menu', {zIndex: "8"});
        gsap.fromTo(".links a", 
                    { opacity: 0, y: 0 }, 
                    { opacity: 1, y:20, delay: 0.25, stagger: 0.25 });
        gsap.set('body', {overflow: "hidden"})                          
    }
    menu.classList.toggle("active");
});

menuLinks.forEach((menuLink) => {
    console.log(menuLink);
    
    menuLink.addEventListener('click', () => {
        console.log('2');
        if (menu.classList.contains("active")) {
            gsap.to(".links", {x: "100%"});
            gsap.to("body", { filter: "grayscale(0)"});
            gsap.set("body", {overflow: "auto"});
            gsap.set("body", {overflowX: "hidden"});
        }
        menu.classList.toggle("active");
    });

});




// set up the API to generate random quotes
async function randomQuote (){
    
    // send a request 
    const response = await fetch("https://api.quotable.io/random");

    // convert the response format 
    const data = await response.json();
    console.log(data);
    return [data.content, data.author]

};

// create a function to update the home page random quote
async function homePageQuote () {

    // call the API function and update the element on the home-page
    const [hQuote, hAuthor] = await randomQuote();
    console.log(hQuote, hAuthor);
    quote.innerText = hQuote;
    author.innerText = hAuthor;
};



// call the function for the first quote
homePageQuote();

// update the home-page quote every 30 seconds
setInterval(homePageQuote, 30000); 


if (grQuoteAddToDb) {
// set up the btn if the user wants to save the generate quote on Generate Random Quote page
    grQuoteAddToDb.addEventListener('click', () => {

        // create a JSON object for grQuote and grAuthor ready to POST to DB upon request
        const grQuoteAddToDbObject = { 
            quote: grQuote.innerHTML,
            author: grAuthor.innerHTML
        };

        console.log(JSON.stringify(grQuoteAddToDbObject));

        // make a POST request to backend and POST the grQuote and grAuthor
        fetch('http://127.0.0.1:5000/random', {
            
            // determine the method 
            method: "POST",

            // create the header and declare it's a JSON posted content with content type application/json
            headers: {
                "Content-Type": "application/json",
            },

            // assign the body of the POST request 
            body: JSON.stringify(grQuoteAddToDbObject),
        });
        alert('The Quote has been saved !')
    });
}
// listen to the user to click the btn 
generateBtn.addEventListener('click', () => {
    randomQuote().then(([q, a]) => {
        console.log(q,a)
        grQuote.innerText  = q;
        grAuthor.innerText = a;
    });
});

// set up the copy btn for review pages
copyBtn.addEventListener("click", () => {
    navigator.clipboard.writeText(reviewQuoteText.innerText)
    console.log("working");
});


// plug in gsap scrolltrigger 
gsap.registerPlugin(ScrollTrigger);

//  set the nav position to fix on scroll when in home-page
if (window.location.href == "http://127.0.0.1:5000/") {
    ScrollTrigger.create({
        trigger: navContainer,
        start: "top -1px",
        onEnter: () => {
            gsap.to(navContainer, {  position: "fixed", zIndex: 2, backgroundColor: "var(--bg-color)"});
            // hrLine.classList.add("scrolled");
        },
        onLeaveBack: () => {
            gsap.set(navContainer, { position: "static", backgroundColor: "transparent" });
            hrLine.classList.remove("scrolled"); 
        },
    });
};

// set up generate btn when the user wants to create a random quote on Generate Random Quote page

// listen to the user to click the btn 
generateBtn.addEventListener('click', () => {
    randomQuote().then(([q, a]) => {
        console.log(q,a)
        grQuote.innerText  = q;
        grAuthor.innerText = a;
    });
});

// menu.addEventListener('click', () => {
//     console.log('11')
//     if (menu.classList.contains("active")) {
//         gsap.to(".links", {x: "100%"});
//         gsap.to("body", { filter: "grayscale(0)"});
//         gsap.set("body", {overflow: "auto"});
//         gsap.set("body", {overflowX: "hidden"});
//     }else{
//         gsap.to(".links", {x: "0%"});
//         gsap.to('#menu', {zIndex: "8"});
//         gsap.to("body", { filter: "grayscale(80%)"});
//         gsap.fromTo(".links a", 
//                     { opacity: 0, y: 0 }, 
//                     { opacity: 1, y:20, delay: 0.25, stagger: 0.25 });
//         gsap.set('body', {overflow: "hidden"})
                          
//     }      
//     menu.classList.toggle("active");
// });

// // set up the btn if the user wants to save the generate quote on Generate Random Quote page
// grQuoteAddToDb.addEventListener('click', () => {

//     // create a JSON object for grQuote and grAuthor ready to POST to DB upon request
//     const grQuoteAddToDbObject = { 
//         quote: grQuote.innerHTML,
//         author: grAuthor.innerHTML
//     };

//     console.log(JSON.stringify(grQuoteAddToDbObject));

//     // make a POST request to backend and POST the grQuote and grAuthor
//     fetch('http://127.0.0.1:5000/random', {
        
//         // determine the method 
//         method: "POST",

//         // create the header and declare it's a JSON posted content with content type application/json
//         headers: {
//             "Content-Type": "application/json",
//         },

//         // assign the body of the POST request 
//         body: JSON.stringify(grQuoteAddToDbObject),
//     });
//     alert('The Quote has been saved !')
// });



