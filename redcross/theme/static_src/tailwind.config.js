/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                lifelink: {
                   
                // Grayyyyyyy
                  gray1: '#D9D9D9',
                  gray2: '#C7BAB9',
                  gray3: '#DADADA',
                  gray4: '#EAEAEA',

                // Blackkkkk
                  black1: '#161616',
                  black2: '#616161',
                  black3: '#474747',
                  black4: '#3E3E3E',
                  black5: '#333333',

                // Redddddd
                   red1: '#D21B16',
                   red2: '#B61611',
                   red3: '#FF0700',

                // gradientttt
                gradient1: 'linear-gradient(to bottom, #D21B16, #FF0700)',
                gradient2: 'linear-gradient(to bottom, #DB392E, #AD0E0A)',
                },
                
                admin: {
                    primary: '#dc3545',
                    secondary: '#007bff',
                    accent: '#ffc107',
                    neutral1: '#f8f9fa',
                    neutral2: '#343a40',
                  },
              },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
