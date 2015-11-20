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
gulp.task('build', ['build:copy_vendor', 'build:copy', 'compile:scss']);

gulp.task('build:copy', (callback) => {
  gulp.src([config.path.src+'/**.html'])
    .pipe(gulp.dest(config.path.dist))
});

gulp.task('build:copy_vendor', (callback) => {
  gulp.src(config.path.vendor+'/**')
    .pipe(gulp.dest(config.path.dist+'/vendor'))
});


gulp.task('compile:scss', (callback) => {
  var sass = require('gulp-sass');
  gulp.src(config.path.src + '/scss/**.scss')
    .pipe(sass())
    .pipe(gulp.dest(config.path.dist + '/css'))
});


/*******************
 * cleanup
 *******************/ 
gulp.task('clean', ['clean:dist']);

gulp.task('clean:dist', (callback) => {
  let fs = require('fs')
  let del = require('del')
  del.sync(config.path.dist)
  fs.mkdirSync(config.path.dist)
});


/*******************
 * Default
 *******************/ 
gulp.task('default', ['build']);
