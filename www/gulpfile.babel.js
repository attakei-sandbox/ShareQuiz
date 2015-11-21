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
gulp.task('build', ['copy:vendor', 'copy:dummy', 'build:copy']);

gulp.task('build:copy', (callback) => {
  var targets = [
    config.path.src+'/**/*.html',
    config.path.src+ '/**/*.css',
    config.path.src+ '/**/*.jsx',
  ];
  gulp.src(targets)
    .pipe(gulp.dest(config.path.out))
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
});

gulp.task('copy:vendor', (callback) => {
  gulp.src(config.path.vendor+'/**')
    .pipe(gulp.dest(config.path.out+'/vendor'))
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
