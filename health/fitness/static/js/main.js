$(function(){
    if($('div').is('.Register')){
        // div class이름이 Register인 페이지에서만 작동
        var fitness_money1 = 800000;
        var fitness_money3 = 900000;
        var fitness_money6 = 1000000;
        var fitness_money12 = 1200000;

    $('#id_피트니스기간').on('change', function(){
        var fitness_option = this.value;
        if(fitness_option == '1개월'){
            $('#결제금액').val(fitness_money1);
        }
        else if(fitness_option == '3개월'){
            $('#결제금액').val(fitness_money3);
        }
        else if(fitness_option == '6개월'){
            $('#결제금액').val(fitness_money6);
        }
        else if(fitness_option == '12개월'){
            $('#결제금액').val(fitness_money12);
        }
    });
    // var pilates_money1 = 800000;
    // var pilates_money3 = 900000;
    // var pilates_money6 = 1000000;
    // var pilates_money12 = 1200000;
    // var money1 = money.toLocaleString(); //3자리수마다 , (왠지모르겠으나 이거하면 폼 전송 실패)
    $('#id_필라테스기간').on('change', function(){
        var pilates_option = this.value;
        if(pilates_option == '주 2회 4주'){
            $('#결제금액').val(10000);
        }
        else if(pilates_option == '주 3회 4주'){
            $('#결제금액').val(20000);
        }
        else if(pilates_option == '주 2회 12주'){
            $('#결제금액').val(30000);
        }
        else if(pilates_option == '주 3회 12주'){
            $('#결제금액').val(40000);
        }
        else if(pilates_option == '주 2회 24주'){
            $('#결제금액').val(50000);
        }
        else if(pilates_option == '주 3회 24주'){
            $('#결제금액').val(60000);
        }
    });
}
});