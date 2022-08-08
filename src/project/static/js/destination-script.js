// Define Variable to element in this page 
let heading_des = $('#heading-destination')

// Method and effect on page 
var text_heading;
heading_des.hover(function(){
    text_heading = heading_des.text();
    heading_des.html('<i class="fas fa-external-link-alt"></i>');
})
heading_des.mouseleave(function(){
    heading_des.text('تركيا');
})