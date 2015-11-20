'use strict';
var gulp = require('gulp');

var config = {
    path: {
        src: './src',
        out: './lib',
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
    .pipe(gulp.dest(config.path.out))
});

gulp.task('build:copy_vendor', (callback) => {
  gulp.src(config.path.vendor+'/**')
    .pipe(gulp.dest(config.path.out+'/vendor'))
});


gulp.task('compile:scss', (callback) => {
  var sass = require('gulp-sass');
  gulp.src(config.path.src + '/scss/**.scss')
    .pipe(sass())
    .pipe(gulp.dest(config.path.out + '/css'))
});


/*******************
 * cleanup
 *******************/ 
gulp.task('clean', ['clean:lib', 'clean:dist']);

gulp.task('clean:lib', (callback) => {
  let fs = require('fs')
  let del = require('del')
  del.sync(config.path.out)
  fs.mkdirSync(config.path.out)
});

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
