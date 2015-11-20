'use strict';
var gulp = require('gulp');

var config = {
    path: {
        src: './src',
        dist: './dist',
        vendor: './vendor',
    }
};


/*******************
 * src -> dist
 *******************/ 
gulp.task('build', ['build:copy_vendor', 'build:copy']);

gulp.task('build:copy', (callback) => {
  gulp.src(config.path.src+'/**')
    .pipe(gulp.dest(config.path.dist))
});

gulp.task('build:copy_vendor', (callback) => {
  gulp.src(config.path.vendor+'/**')
    .pipe(gulp.dest(config.path.dist+'/vendor'))
});


/*******************
 * Default
 *******************/ 
gulp.task('default', ['build']);
