const LoginFunctions = {
   
    // Function to display Login Area on click
    openLog: function displayLogin (id) {
        var x = document.getElementById (id);
        x.style.display = 
        ((x.style.display != 'none') ? 'none' : 'block');
    },
    
    // Function to close Login Area on click of 'X'
    closeLog: function closeLogin (id) {
        var x = document.getElementById (id);
        x.style.display = 'none';
    },
    
    // Function to display Register Area on click
    openReg: function displayReg (id) {
        var x = document.getElementById (id);
        x.style.display =
        ((x.style.display != 'none') ? 'none' : 'block');
    },
    
    // Function to close Register Area on click of 'X'
    closeReg: function closeReg (id) {
	    var x = document.getElementById (id);
	    x.style.display = 'none';
    },

    // Function to open Landing Area of click of button
    openLand: function openLand (id) {
        var x = document.getElementById (id);
        x.style.display =
        ((x.style.display != 'none') ? 'none' : 'flex'); 
    },

    // Function to close Landing Area on click of 'X'
    closeLand: function closeLand (id) {
        var x = document.getElementById(id);
        x.style.display = 'none';
    }
}

//module.exports = LoginFunctions;

/* Function to close/shorten Left Side Bar on-click -- UNFINISHED
function trimSideBar (id) {
	var x = document.getElementById(id);
	x.style.di
} */