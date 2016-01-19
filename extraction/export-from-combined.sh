#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

srcFn="$1"
destDir="$2"

key=$(basename -s ".svg" -z "${srcFn}")

echo "Exporting icon ${key} from ${srcFn} to ${destDir}"

function export {
    res=$1
    area=$2
    pngFile="${destDir}/${res}/${key}.png"
    inkscape --export-png="${pngFile}" -a "${area}" "${srcFn}"

    pngcrush -ow -q -brute "${pngFile}"
}

#export resolutions
export 16 "96:0:112:16"
export 22 "96:20:118:42"
export 24 "95:19:119:43"
export 32 "96:45:128:77"
export 48 "96:77:144:125"

dest96="${destDir}/96/${key}.svg"

# split out the 96px svg
${DIR}/extract-group.py -i ${srcFn} -o "${dest96}" -l "96px"

inkscape --vacuum-defs "${dest96}"

