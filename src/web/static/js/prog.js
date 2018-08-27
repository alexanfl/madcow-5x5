$(window).load( () => {
  $( () => {
    $('#squat_primary').bootstrapTable({ 
      data: data.squat_primary,
      columns: columns,
      formatLoadingMessage: () => {
          return ''
      },
      formatShowingRows: () => {
          return ''
      },
    }); 
    $('#bench_primary').bootstrapTable({ 
      data: data.bench_primary,
      columns: columns,
      formatLoadingMessage: () => {
          return ''
      },
      formatShowingRows: () => {
          return ''
      },
    }); 
    $('#row_primary').bootstrapTable({ 
      data: data.row_primary,
      columns: columns,
      formatLoadingMessage: () => {
          return ''
      },
      formatShowingRows: () => {
          return ''
      },
    }); 
  });
});

function dataFormatter(value, row, index, field) {
    if (value) {
      html = [value]; 
    }
    else {
        html = ['-']
    }
    return html.join('');
}
