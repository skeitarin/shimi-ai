$(function () {
    // initialize materializecss
    $('select').formSelect();
    $('.modal').modal();

    $('#btn_judge').on('click', function(){
        $('#txt_result').text("predicting...");
        var param_arry = [];
        for(var i = 0; i < 5; i++){
            var pat = $('#form_judge [name=pat_' + i.toString() + ']').val();
            var num = $('#form_judge [name=num_' + i.toString() + ']').val();
            param_arry.push(pat)
            param_arry.push(num)
        }
        $.ajax({
            url: '/poker/predict',
            type: 'POST',    
            dataType: "text",
            contentType: "application/json",  
            data: JSON.stringify(param_arry)    
        })
        .done(function (data) {
            console.log(data);
            $('#txt_result').text(data);
        })
        .fail(function(data) {
            console.log(data)
            alert('error!!');
        })
    })
})  