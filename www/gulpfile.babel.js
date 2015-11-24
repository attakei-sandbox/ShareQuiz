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
var appConfig = require('config');


/*******************
 * src -> dist
 *******************/ 
gulp.task('build', ['copy:vendor', 'copy:dummy', 'compile:ect', 'build:copy']);

gulp.task('build:copy', (callback) => {
  var targets = [
    config.path.src+'/**/*.html',
    config.path.src+ '/**/*.css',
    config.path.src+ '/**/*.jsx',
  ];
  gulp.src(targets)
    .pipe(gulp.dest(config.path.out))
  callback();
});

gulp.task('compile:ect', (callback) => {
  var ect = require('gulp-ect');
  gulp.src(config.path.src + '/**.ect')
    .pipe(ect({data: appConfig}))
    .pipe(gulp.dest(config.path.out));
  callback();
});

gulp.task('compile:scss', (callback) => {
  var sass = require('gulp-sass');
  gulp.src(config.path.src + '/scss/**.scss')
    .pipe(sass())
    .pipe(gulp.dest(config.path.out + '/css'))
});

gulp.task('copy:dummy', (callback) => {
  gulp.src([config.path.src+'/dmy/**'])
    .pipe(gulp.dest(config.path.out+'/dmy'))
  callback();
});

gulp.task('copy:vendor', (callback) => {
  gulp.src(config.path.vendor+'/**')
    .pipe(gulp.dest(config.path.out+'/vendor'))
  callback();
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
 * watching
 *******************/ 
gulp.task('watch', ['build'], () => {
  gulp.watch('./src/**', ['build']);
});


/*******************
 * Default
 *******************/ 
gulp.task('default', ['build']);
