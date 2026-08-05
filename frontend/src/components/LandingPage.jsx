import React from "react";
import { motion } from "framer-motion";
import { HeroText, Body, Label } from "./Typography";
import { Button } from "./Button";
import { ArrowDown } from "lucide-react";

// export const LandingPage = () => {
//   const containerVariants = {
//     hidden: { opacity: 0 },
//     show: {
//       opacity: 1,
//       transition: {
//         staggerChildren: 0.15,
//         delayChildren: 0.2,
//       },
//     },
//   };

//   const itemVariants = {
//     hidden: { opacity: 0, y: 30 },
//     show: {
//       opacity: 1,
//       y: 0,
//       transition: { duration: 0.6, ease: [0.25, 0, 0, 1] },
//     },
//   };

//   return (
//     <div className="min-h-screen w-full flex flex-col justify-center items-center py-12 px-6 md:px-12 lg:px-16 bg-black text-white border-b border-zinc-900 overflow-hidden">
//       <motion.div
//         variants={containerVariants}
//         initial="hidden"
//         animate="show"
//         className="w-full max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-x-8 lg:gap-x-12 gap-y-12 items-center my-auto"
//       >
//         {/* Left Column: Axiom-Scale Logo Badge Area */}
//         <motion.div
//           variants={itemVariants}
//           className="col-span-1 md:col-span-6 lg:col-span-5 flex justify-center md:justify-start items-center"
//         >
//           <div className="relative w-full max-w-[420px] lg:max-w-[480px] aspect-[16/9] flex items-center justify-center border border-dashed border-zinc-800 bg-zinc-950/40 rounded-full group hover:border-[#5568fe]/50 transition-colors">
//             <img
//               src="/logo.png"
//               alt="Compass Logo"
//               className="w-full h-full object-contain p-2 opacity-95 transition-opacity group-hover:opacity-100"
//               onError={(e) => {
//                 e.currentTarget.style.display = "none";
//               }}
//             />
//             {/* Fallback overlay label */}
//             <span className="absolute font-mono text-xs uppercase tracking-widest text-zinc-600 pointer-events-none">
//               [ Logo Space ]
//             </span>
//           </div>
//         </motion.div>

//         {/* Right Column: Hero Typography & Navigation */}
//         <div className="col-span-1 md:col-span-6 lg:col-span-7 flex flex-col items-start text-left space-y-8 lg:space-y-10">
//           {/* Label Section */}
//           <motion.div
//             variants={itemVariants}
//             className="flex flex-col items-start space-y-1"
//           >
//             <Label className="text-[#5568fe] inline-block font-mono text-xs md:text-lg lg:text-xl mb-1 mt-4 md:mt-0 tracking-[0.25em] uppercase font-bold">
//               WELCOME TO COMPASS
//             </Label>
//             <span className="text-zinc-500 font-mono text-[11px] sm:text-xs tracking-[0.2em] uppercase">
//               INTELLIGENT CODEBASE INTELLIGENCE
//             </span>
//           </motion.div>

//           {/* Hero Typography */}
//           <motion.div variants={itemVariants} className="w-full">
//             <HeroText className="text-5xl sm:text-6xl md:text-7xl lg:text-[7.5rem] leading-[0.9]">
//               NavigateAny <br />
//               <span className="text-slate-500">Codebase.</span>
//             </HeroText>
//           </motion.div>

//           {/* Subtitle */}
//           <motion.div variants={itemVariants} className="w-full max-w-xl">
//             <Body className="text-zinc-400 text-lg sm:text-xl md:text-2xl font-normal leading-relaxed">
//               Compass provides direct access to repository architecture, file
//               dependencies, and interactive code analysis.
//             </Body>
//           </motion.div>

//           {/* Scroll Anchor Action */}
//           <motion.div variants={itemVariants} className="pt-2">
//             <Button
//               variant="ghost"
//               type="button"
//               className="px-0 text-[#5568fe]  gap-2 text-base uppercase tracking-[0.2em] hover:text-[#7887ff] md:text-lg px-8 py-6 font-bold flex items-center gap-3 bg-transparent border-none transition-colors group"
//               onClick={() => {
//                 document
//                   .getElementById("analysis-section")
//                   ?.scrollIntoView({ behavior: "smooth" });
//               }}
//             >
//               <span>EXPLORE ANALYSIS</span>
//               <ArrowDown
//                 className="w-5 h-5 pointer-events-none ml-2"
//                 strokeWidth={1.5}
//               />
//             </Button>

//             <div className="pt-8 -mt-10 md:pt-12">
//               <Button
//                 variant="primary"
//                 className="gap-2  md:text-lg "
//                 onClick={() => {
//                   document
//                     .getElementById("tutors-section")
//                     ?.scrollIntoView({ behavior: "smooth" });
//                 }}
//               ></Button>
//             </div>
//           </motion.div>
//         </div>
//       </motion.div>
//     </div>
//   );
// };

export const LandingPage = () => {
  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    show: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6, ease: [0.25, 0, 0, 1] },
    },
  };

  return (
    <div className="min-h-screen w-full flex flex-col justify-center items-center py-12 px-6 md:px-12 lg:px-16 bg-black text-white border-b border-zinc-900 overflow-hidden">
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="show"
        className="w-full max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-x-8 lg:gap-x-12 gap-y-12 items-center my-auto"
      >
        {/* Left Column: Axiom-Scale Logo Badge Area */}
        <motion.div
          variants={itemVariants}
          className="col-span-1 md:col-span-6 lg:col-span-5 flex justify-center md:justify-start items-center"
        >
          <div className="relative w-full max-w-[420px] lg:max-w-[480px] aspect-[16/9] flex items-center justify-center border border-dashed border-zinc-800 bg-zinc-950/40 rounded-full group hover:border-[#5568fe]/50 transition-colors">
            <img
              src="/logo.png"
              alt="Compass Logo"
              className="w-full h-full object-contain p-2 opacity-95 transition-opacity group-hover:opacity-100"
              onError={(e) => {
                e.currentTarget.style.display = "none";
              }}
            />
            {/* Fallback overlay label */}
            <span className="absolute font-mono text-xs uppercase tracking-widest text-zinc-600 pointer-events-none">
              [ Logo Space ]
            </span>
          </div>
        </motion.div>

        {/* Right Column: Hero Typography & Navigation */}
        <div className="col-span-1 md:col-span-6 lg:col-span-7 flex flex-col items-start text-left space-y-8 lg:space-y-10">
          {/* Label Section */}
          <motion.div
            variants={itemVariants}
            className="flex flex-col items-start space-y-1"
          >
            <Label className="text-[#5568fe] inline-block font-mono text-xs md:text-lg lg:text-xl mb-1 mt-4 md:mt-0 tracking-[0.25em] uppercase font-bold">
              WELCOME TO COMPASS
            </Label>
            <span className="text-zinc-500 font-mono text-[11px] sm:text-xs tracking-[0.2em] uppercase">
              INTELLIGENT CODEBASE INTELLIGENCE
            </span>
          </motion.div>

          {/* Hero Typography */}
          <motion.div variants={itemVariants} className="w-full">
            <HeroText className="text-5xl sm:text-6xl md:text-7xl lg:text-[7.5rem] leading-[0.9]">
              NavigateAny <br />
              <span className="text-slate-500">Codebase.</span>
            </HeroText>
          </motion.div>

          {/* Subtitle */}
          <motion.div variants={itemVariants} className="w-full max-w-xl">
            <Body className="text-zinc-400 text-lg sm:text-xl md:text-2xl font-normal leading-relaxed">
              Compass provides direct access to repository architecture, file
              dependencies, and interactive code analysis.
            </Body>
          </motion.div>

          {/* Scroll Anchor Action */}
          <motion.div variants={itemVariants} className="pt-2">
           
            <Button
              variant="ghost"
              type="button"
              className="relative px-0 text-[#5568fe] hover:text-[#7887ff] font-mono text-base md:text-lg uppercase tracking-[0.2em] font-bold flex items-center gap-3 bg-transparent border-none transition-colors group cursor-pointer pb-2"
              onClick={() => {
                document
                  .getElementById("explore-section")
                  ?.scrollIntoView({ behavior: "smooth" });
              }}
            >
              <span>EXPLORE ANALYSIS</span>
              <ArrowDown
              //  className="px-0 text-[#5568fe] gap-2 text-base uppercase tracking-[0.2em] hover:text-[#7887ff] md:text-lg px-8 py-6 font-bold flex items-center gap-3 bg-transparent border-none transition-colors group cursor-pointer"
                className="w-5 h-5 pointer-events-none transition-transform group-hover:translate-y-1"
                strokeWidth={2}
              />

              {/* Hover Animated Underline */}
              <span
                className="absolute -bottom-3 left-1/2 -translate-x-1/2 w-80 group-hover:w-full h-[2px] bg-[#5568fe] group-hover:bg-[#7887ff] transition-all duration-300 ease-out pointer-events-none"
                strokeWidth={1.5}
              />
            </Button>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
};
