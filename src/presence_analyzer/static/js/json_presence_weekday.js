(function($) {
    $(document).ready(function(){
        var loading = $('#loading');
        var users = [];
        $.getJSON("/api/v2/users", function(result) {
            var dropdown = $("#user_id");
            $.each(result, function(item) {
                dropdown.append($("<option />").val(item).text(this.name).attr('data-avatar', this.avatar));
            });
            users = result;
            dropdown.show();
            loading.hide();
        });
        $('#user_id').change(function(){
            var selected_user = $("#user_id").val();
            var avatar = $('#user_id').data('avatar');
            var chart_div = $('#chart_div');
            if(selected_user) {
                var newImage = users[selected_user]['avatar'];
                var user = users[selected_user]['user_id'];
                $('#avatar').children('img').attr('src', newImage);
                loading.show();
                chart_div.hide();
                $.getJSON("/api/v1/presence_weekday/"+user, function(result) {
                    if(result.length !== 0){
                        var data = google.visualization.arrayToDataTable(result);
                        var options = {};
                        chart_div.show();
                        loading.hide();
                        var chart = new google.visualization.PieChart(chart_div[0]);
                        chart.draw(data, options);
                    }
                    else{
                        chart_div.show();
                        $('#chart_div').text('Brak danych dla tego użytkownika');
                        loading.hide();
                    }            
                });
            }
        });
    });
})(jQuery);
