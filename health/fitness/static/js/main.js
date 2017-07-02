$(function(){
    if($('div').is('.Register')){

        //종류선택시 tr 없애고 나타내기
        $('#type_choice').on('change', function(){
            var choice_option = this.value;

            if(choice_option=='Fitness'){
                $('#tr_period_fitness').css("display","");
                $('#tr_period_pilates').css("display","none");
                $('#tr_period_both').css("display","none");
            }
            else if(choice_option=='Pilates'){
                $('#tr_period_fitness').css("display","none");
                $('#tr_period_pilates').css("display","");
                $('#tr_period_both').css("display","none");
            }
            else if(choice_option=='Both'){
                $('#tr_period_fitness').css("display","none");
                $('#tr_period_pilates').css("display","none")
                $('#tr_period_both').css("display","");
            }

        });
        // div class이름이 Register인 페이지에서만 작동
        var B1 = 200000;
        var B3 = 390000;
        var B6 = 630000;
        var B12 = 960000;

    //피트니스기간선택에 따른 결제금액 변경
    $('#period_fitness').on('change', function(){
        var fitness_option = this.value;
        if(fitness_option == "m1"){
            $('#payment_amount').val(B1);
        }
        else if(fitness_option == 'm3'){
            $('#payment_amount').val(B3);
        }
        else if(fitness_option == 'm6'){
            $('#payment_amount').val(B6);
        }
        else if(fitness_option == 'm12'){
            $('#payment_amount').val(B12);
        }

    });
    // var pilates_money1 = 800000;
    // var money1 = money.toLocaleString(); //3자리수마다 , (왠지모르겠으나 이거하면 폼 전송 실패)
    //
    // 필라테스기간선택에 따른 결제금액 변경
    // 지금 필라테스선택시 가입이 안됌..
    $('#period_pilates').on('change', function(){
        var pilates_option = this.value;
        if(pilates_option == 'se2m1'){
            $('#payment_amount').val(216000);
        }
        else if(pilates_option == 'se3m1'){
            $('#payment_amount').val(300000);
        }
        else if(pilates_option == 'se2m3'){
            $('#payment_amount').val(528000);
        }
        else if(pilates_option == 'se3m3'){
            $('#payment_amount').val(720000);
        }
        else if(pilates_option == 'se2m6'){
            $('#payment_amount').val(912000);
        }
        else if(pilates_option == 'se3m6'){
            $('#payment_amount').val(1224000);
        }
    });

    //등급 받기
    $('#rating').on('change', function(){
        rating = this.value; //var없으면 function안에 있어도 전역변수
    });

    //필라테스+피트니스 선택시, 등급과 기간에 따른 금액 변경
    //하지만, 아직 등급을 바꾸면 다시 기간을 선택해야 제대로 적용되는 난점 있음.
    $('#period_both').on('change', function(){
        both_option =this.value;

        if(rating=='B'){
            if(both_option == 'se2m1'){
                $('#payment_amount').val(286000);
            }
            else if(both_option=='se3m1'){
                $('#payment_amount').val(370000);
            }
            else if(both_option=='se2m3'){
                $('#payment_amount').val(570000);
            }
            else if(both_option=='se3m3'){
                $('#payment_amount').val(750000);
            }
            else if(both_option=='se2m6'){
                $('#payment_amount').val(2040000);
            }
            else if(both_option=='se3m6'){
                $('#payment_amount').val(2760000);
            }
            else{

            }

        }
        if(rating=='S'){
            if(both_option == 'se2m1'){
                $('#payment_amount').val(316000);
            }
            else if(both_option=='se3m1'){
                $('#payment_amount').val(400000);
            }
            else if(both_option=='se2m3'){
                $('#payment_amount').val(660000);
            }
            else if(both_option=='se3m3'){
                $('#payment_amount').val(840000);
            }
            else if(both_option=='se2m6'){
                $('#payment_amount').val(2160000);
            }
            else if(both_option=='se3m6'){
                $('#payment_amount').val(2880000);
            }
            else{

            }
        }
});


}

if($('div').is('.PT_Register')){
    $('#registered_session').on('change', function(){
        registered_session = this.value; //var없으면 function안에 있어도 전역변수
    });

    $("#PT_payment_amount").keyup(function(event){
        // 결제금액/횟수 = 1회세션단가
        var result = (this.value)/registered_session;
        //1회세션단가에 값 넣어주기
        $('#unitprice').val(result);
    });

}
});